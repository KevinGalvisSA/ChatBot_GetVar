from app.infrastructure.factories.langraph_orchestator import LangraphOrchestrator
from app.infrastructure.factories.qdrant import QdrantService
from app.infrastructure.factories.gemini_integration import answer_with_gemini
from app.infrastructure.sql.setupDB import ChatMessageHistory
from app.infrastructure.sql.message_saver import save_message  # Asegúrate de importar esto correctamente
from app.config.bot_regulations import BotRegulations
import os
import re
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "asesorias")
qdrant_api_key = os.getenv("QDRANT_API_KEY", "")

if not qdrant_url or not qdrant_collection_name or not qdrant_api_key:
    raise ValueError("Faltan variables de entorno. Asegúrate de definir QDRANT_URL, QDRANT_COLLECTION_NAME y QDRANT_API_KEY en el archivo .env")

qdrant_service = QdrantService(
    url=qdrant_url,
    collection_name=qdrant_collection_name,
    api_key=qdrant_api_key
)

orchestrator = LangraphOrchestrator(
    qdrant_url=qdrant_url,
    qdrant_collection_name=qdrant_collection_name,
    qdrant_api_key=qdrant_api_key
)

def extract_name_and_phone(text: str):
    # Buscar el nombre con distintas formas comunes
    name_match = re.search(r"(?i)(mi nombre es|soy|me llamo)\s+([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+)", text)
    
    # Buscar teléfono en múltiples formatos
    phone_match = re.search(r"(?i)(número|numero).{0,20}(\d{4,15})", text)

    name = name_match.group(2).strip() if name_match else None
    phone = phone_match.group(2).strip() if phone_match else None

    return {"name": name, "phone": phone}


def chat_with_bot(user_input: str, session_id: str) -> str:
    print("🟡 chat_with_bot iniciado")
    print(f"📥 Mensaje recibido: {user_input}")
    print(f"🆔 session_id recibido: {session_id}")

    name_known = BotRegulations.user_input.get("name")
    phone_known = BotRegulations.user_input.get("phone")
    print(f"📌 Nombre conocido: {name_known}, Teléfono conocido: {phone_known}")

    if not name_known or not phone_known:
        print("🔎 Usuario aún no identificado. Ejecutando LangGraph...")

        response = orchestrator.run(user_input)
        print(f"🔁 Respuesta inicial del orquestador: {response}")

        # EXTRAEMOS MANUALMENTE nombre y teléfono
        extracted = extract_name_and_phone(user_input)
        print(f"🧪 Datos extraídos (manual regex): {extracted}")

        if extracted.get("name") and extracted.get("phone"):
            BotRegulations.user_input = {
                "name": extracted["name"],
                "phone": extracted["phone"]
            }
            print(f"✅ Datos del usuario guardados: {BotRegulations.user_input}")
            return f"✅ ¡Gracias, {extracted['name']}! Ahora dime, ¿en qué puedo ayudarte?"

        print("⚠️ No se pudieron extraer datos de identificación. Retornando respuesta simple.")
        return response

    # Si ya tenemos los datos del usuario, se usa el historial persistente con Gemini
    print("🧠 Usuario identificado. Recuperando historial...")
    chat_history = ChatMessageHistory(session_id=session_id)
    history = chat_history.get_messages()

    print(f"📜 Historial recuperado ({len(history)} mensajes): {[m.content for m in history]}")
    messages = [m.content for m in history]

    response = answer_with_gemini(user_input, messages)
    print(f"🤖 Respuesta generada por Gemini: {response}")

    chat_history.add_user_message(user_input)
    chat_history.add_ai_message(response)

    try:
        print("📥 Guardando en tabla messageStorage")
        id_customer = 1  # Este ID puede ser dinámico luego
        # Guardar mensaje del usuario
        save_message(id_customer=id_customer, session_id=int(session_id), content=user_input, message_type="human")

# Guardar mensaje del bot
        save_message(id_customer=id_customer, session_id=int(session_id), content=response, message_type="ai")

        print(f"✅ Mensajes guardados exitosamente para session_id={session_id}")
    except Exception as e:
        print(f"❌ Error guardando en messageStorage: {e}")

    return response




def capture_user_data(user_input: str) -> str | None:
    """
    Captura rápida de nombre y teléfono si el usuario lo proporciona directamente.
    """
    try:
        lower_msg = user_input.lower()
        if "mi nombre es" in lower_msg and "mi numero de telefono es" in lower_msg:
            parts = user_input.split("y mi numero de telefono es")
            name = parts[0].replace("Mi nombre es", "").strip()
            phone = parts[1].strip()

            BotRegulations.user_input = {
                "name": name,
                "phone": phone
            }

            print("✅ Datos capturados:", BotRegulations.user_input)
            return None

    except Exception as e:
        print(f"❌ Error capturando datos: {e}")

    return None
