from app.infrastructure.factories.qdrant import QdrantService
from app.infrastructure.factories.gemini_integration import answer_with_gemini
from app.infrastructure.sql.setupDB import ChatMessageHistory, get_customer_by_phone
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

def chat_with_bot(user_input: str, session_id: str) -> str:
    print("📥 Iniciando chat_with_bot")
    print(f"📝 Entrada del usuario: {user_input}")
    print(f"🆔 session_id: {session_id}")

    # 1️⃣ Extraer nombre y teléfono del texto
    extracted_info = extractor.extract(user_input)
    name = extracted_info.get("name")
    phone = extracted_info.get("phone")

    print(f"🔍 Extraído ➜ nombre: {name}, teléfono: {phone}")

    if name:
        BotRegulations.user_input["name"] = name
    if phone:
        BotRegulations.user_input["phone"] = phone

    # 2️⃣ Obtener teléfono conocido
    phone_known = BotRegulations.user_input.get("phone")

    # 3️⃣ Fallback: usar session_id como teléfono si no se extrajo
    if not phone_known and session_id.isdigit():
        print(f"📲 Usando session_id como fallback de teléfono: {session_id}")
        phone_known = session_id

    # 4️⃣ Buscar o crear cliente (solo si hay teléfono válido)
    id_customer = 0
    name_known = None  # Inicializa aquí por claridad
    if phone_known:
        try:
            phone_num = int(phone_known)
            print(f"🔍 Buscando o creando cliente con teléfono: {phone_num}")
            customer = get_or_create_customer(name=BotRegulations.user_input.get("name"), phone=phone_num) # type: ignore
            id_customer = customer.id if customer else 0
            # Forzar a que sea el nombre ubicado en customer.name
            BotRegulations.user_input["name"] = customer.name
            name_known = customer.name  # ✅ Actualiza la variable con el valor real
            print("El nombre del customer es:", name_known)
        except Exception as e:
            print(f"❌ Error en get_or_create_customer: {e}")
    else:
        print("⚠️ Teléfono no válido. Cliente no será creado.")

    print(f"📌 Datos finales ➜ nombre: {name_known}, teléfono: {phone_known}")

    # 5️⃣ Buscar contexto en Qdrant
    try:
        context_chunks = qdrant_service.search(user_input)
    except Exception as e:
        print(f"❌ Error en búsqueda Qdrant: {e}")
        context_chunks = []

    # 6️⃣ Generar respuesta desde Gemini con historial
    try:
        chat_history = ChatMessageHistory(session_id=session_id, id_customer=id_customer) # type: ignore
        messages = chat_history.get_messages()

        print("Estos son los mensajes:", messages)

        formatted_history = "\n".join([
            f"Usuario: {m.content}" if m.type == "human" else f"Bot: {m.content}"
            for m in messages
        ])

        estado_sesion = "\n".join([
            f"{clave.capitalize()}: {valor}" for clave, valor in BotRegulations.user_input.items() if valor
        ])

        prompt_con_historial = (
            f"[ESTADO DE SESIÓN]\n{estado_sesion}\n\n"
            f"[HISTORIAL DE CONVERSACIÓN]\n{formatted_history}\n\n"
            f"[NUEVO MENSAJE DEL USUARIO]\n{user_input}"
        )

        print("🧠 Prompt completo para Gemini:\n", prompt_con_historial)
        response = answer_with_gemini(question=prompt_con_historial, chunks=context_chunks)

    except Exception as e:
        print(f"❌ Error usando Gemini: {e}")
        response = f"❌ Error al usar el Gemini: {str(e)}"

    return response



def generate_chat_summary(session_id: str) -> str:
    try:
        # Obtener número como int
        phone = int(session_id)

        # Validar cliente
        customer = get_customer_by_phone(phone)
        if not customer:
            return "❌ No se encontró un cliente con ese número."

        # Historial del cliente
        history = ChatMessageHistory(
            session_id=session_id,
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