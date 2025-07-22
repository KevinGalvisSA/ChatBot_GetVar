from app.infrastructure.factories.qdrant import QdrantService
from app.infrastructure.factories.gemini_integration import answer_with_gemini
from app.infrastructure.sql.setupDB import ChatMessageHistory
from app.infrastructure.sql.message_saver import save_message
from app.infrastructure.factories.extract_info import InfoExtractor
from app.config.bot_regulations import BotRegulations
from app.infrastructure.sql.customer_saver import get_or_create_customer
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar servicios
qdrant_service = QdrantService(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    collection_name=os.getenv("QDRANT_COLLECTION_NAME", "asesorias"),
    api_key=os.getenv("QDRANT_API_KEY", "")
)

extractor = InfoExtractor()

def chat_with_bot(user_input: str, session_id: str) -> str:
    # Extraer información del usuario (nombre y teléfono)
    extracted_info = extractor.extract(user_input)
    name = extracted_info.get("name")
    phone = extracted_info.get("phone")

    if name:
        BotRegulations.user_input["name"] = name
    if phone:
        BotRegulations.user_input["phone"] = phone

    name_known = BotRegulations.user_input.get("name")
    phone_known = BotRegulations.user_input.get("phone")
    phone_num = int(phone_known) if phone_known else 0

    # Obtener o crear cliente
    try:
        customer = get_or_create_customer(name=name_known, phone_number=phone_num)
        id_customer = customer.id if customer else 0
    except Exception as e:
        print(f"❌ Error en get_or_create_customer: {e}")
        id_customer = 0

    # Buscar contexto en Qdrant
    try:
        context_chunks = qdrant_service.search(user_input)
    except Exception as e:
        print(f"❌ Error en búsqueda Qdrant: {e}")
        context_chunks = []

    # Obtener respuesta desde Gemini (⚠️ aquí corregimos el keyword argument)
# Obtener respuesta desde Gemini usando historial de mensajes
    try:
        # 1️⃣ Recuperar historial desde la base de datos
        chat_history = ChatMessageHistory(session_id=session_id, id_customer=id_customer)
        messages = chat_history.get_messages()

    # 2️⃣ Formatear el historial como texto plano
        formatted_history = "\n".join([
        f"Usuario: {m.content}" if m.type == "human" else f"Bot: {m.content}"
        for m in messages
        ])

    # 3️⃣ Combinar historial + input actual
        prompt_con_historial = f"{formatted_history}\nUsuario: {user_input}"

    # 4️⃣ Enviar a Gemini como una sola entrada
        response = answer_with_gemini(question=prompt_con_historial, chunks=context_chunks)

    except Exception as e:
        response = f"❌ Error al usar Gemini: {str(e)}"


    # Guardar mensajes en la base de datos
    try:
        save_message(id_customer=id_customer, session_id=int(session_id), content=user_input, message_type="human")
        save_message(id_customer=id_customer, session_id=int(session_id), content=response, message_type="ai")
    except Exception as e:
        print(f"❌ Error guardando en messageStorage: {e}")

    return response