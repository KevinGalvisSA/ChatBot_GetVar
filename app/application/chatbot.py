from app.infrastructure.langraph_orchestator import LangraphOrchestrator
from app.infrastructure.qdrant import QdrantService
from app.infrastructure.gemini_integration import answer_with_gemini
from app.infrastructure.sql.setupDB import ChatMessageHistory  # ✅ NUEVO
from app.config.bot_regulations import BotRegulations
import os
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


def chat_with_bot(user_input: str, session_id: str) -> str:
    """
    Función central del chatbot con memoria persistente y extracción de datos.
    """

    # Si el usuario no ha sido identificado aún
    if not BotRegulations.user_input.get("name") or not BotRegulations.user_input.get("phone"):
        response = orchestrator.run(user_input)
        extracted = orchestrator.info_extractor.extract(user_input)

        if extracted.get("name") and extracted.get("phone"):
            BotRegulations.user_input = {
                "name": extracted["name"],
                "phone": extracted["phone"]
            }
            return f"✅ ¡Gracias, {extracted['name']}! Ahora dime, ¿en qué puedo ayudarte?"

        return response

    # Si ya tenemos los datos del usuario, se usa el historial persistente con Gemini
    chat_history = ChatMessageHistory(session_id=session_id)
    history = chat_history.get_messages()
    messages = [m.content for m in history]

    response = answer_with_gemini(user_input, messages)

    chat_history.add_user_message(user_input)
    chat_history.add_ai_message(response)

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
