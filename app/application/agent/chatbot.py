from app.infrastructure.factories.qdrant import QdrantService
from app.infrastructure.factories.gemini_integration import answer_with_gemini
from app.infrastructure.sql.setupDB import ChatMessageHistory, get_customer_by_phone_number
from app.infrastructure.sql.message_saver import save_message
from app.infrastructure.factories.extract_info import InfoExtractor
from app.config.bot_regulations import BotRegulations
from app.infrastructure.sql.customer_saver import get_or_create_customer
from langchain_core.messages import HumanMessage
from app.models.context_chunk import ContextChunk
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

def chat_with_bot(user_input: str, id_session: str) -> str:
    # Extraer información del usuario (nombre y teléfono)
    extracted_info = extractor.extract(user_input)
    name = extracted_info.get("name")
    phone_number = extracted_info.get("phone_number")

    if name:
        BotRegulations.user_input["name"] = name
    if phone_number:
        BotRegulations.user_input["phone_number"] = phone_number

    name_known = BotRegulations.user_input.get("name")
    phone_number_known = BotRegulations.user_input.get("phone_number")
    phone_number_num = int(phone_number_known) if phone_number_known else 0

    # Obtener o crear cliente
    try:
        customer = get_or_create_customer(name=name_known, phone_number_number=phone_number_num) # type: ignore
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
        chat_history = ChatMessageHistory(id_session=id_session, id_customer=id_customer) # type: ignore
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
        response = f"❌ Error al usar el Gemini: {str(e)}"


    # Guardar mensajes en la base de datos
    try:
        save_message(id_customer=id_customer, id_session=int(id_session), content=user_input, message_type="human") # type: ignore
        save_message(id_customer=id_customer, id_session=int(id_session), content=response, message_type="ai") # type: ignore
    except Exception as e:
        print(f"❌ Error guardando en messageStorage: {e}")

    return response

def generate_chat_summary(id_session: str) -> str:
    try:
        # Obtener número como int
        phone_number_number = int(id_session)

        # Validar cliente
        customer = get_customer_by_phone_number(phone_number_number)
        if not customer:
            return "❌ No se encontró un cliente con ese número."

        # Historial del cliente
        history = ChatMessageHistory(
            id_session=id_session,
            id_customer=customer.id  # type: ignore si es necesario
        )

        messages = history.get_messages()
        if not messages:
            return "❌ No hay mensajes para generar un resumen."

        # Armar historial con formato limpio
        formatted_history = "\n".join([
            f"Usuario: {m.content}" if isinstance(m, HumanMessage) else f"Bot: {m.content}"
            for m in messages
        ])

        # Crear el chunk con score dummy
        resumen = answer_with_gemini(
            question="Resume la siguiente conversación brevemente.",
            chunks=[ContextChunk(text=formatted_history, score=1.0)]
        )

        return resumen

    except Exception as e:
        print(f"❌ Error generando resumen: {e}")
        return "❌ Error interno al generar resumen."