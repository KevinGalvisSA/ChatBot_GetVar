from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.sql.message_saver import get_messages_by_session, save_message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SaveMessageInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")
    message_content: str = Field(description="Contenido del mensaje")
    message_type: str = Field(description="Tipo de mensaje (ej. 'human', 'ai')")

@tool(args_schema=SaveMessageInput)
def save_message_tool(state: dict, message_content: str, message_type: str) -> dict:
    """
    Guarda un mensaje nuevo en la BD y retorna el historial actualizado.
    """
    try:
        session_id = state.get("session_id")
        customer_id = state.get("customer_id")

        if not session_id or not customer_id:
            logger.warning("⚠️ No se proporcionó session_id o customer_id en el state.")
            return {"history_messages": state.get("history_messages", [])}

        # Guardar el mensaje actual
        save_message(
            id_customer=customer_id,
            session_id=str(session_id),
            content=message_content,
            message_type=message_type
        )

        # Recargar historial actualizado (limite de 15)
        messages = get_messages_by_session(
            session_id=session_id,
            id_customer=customer_id,
            limit=15
        )

        history_list = [
            {"message": str(msg.message), "type": str(msg.message_type)}
            for msg in messages
        ]

        logger.info(f"📜 Historial actualizado ({len(history_list)} mensajes).")
        return {"history_messages": history_list}

    except Exception as e:
        logger.error(f"❌ Error en save_message_tool: {e}")
        return {"history_messages": state.get("history_messages", [])}


class GetHistoryInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=GetHistoryInput)
def get_history_tool(state: dict) -> dict:
    """
    Obtiene los últimos 15 mensajes del historial para el cliente y sesión.
    """
    try:
        session_id = state.get("session_id")
        customer_id = state.get("customer_id")

        if not session_id or not customer_id:
            logger.warning("⚠️ No se proporcionó session_id o customer_id en el state.")
            return {"history_messages": []}

        messages = get_messages_by_session(
            session_id=session_id,
            id_customer=customer_id,
            limit=15
        )

        history_list = [
            {"message": str(msg.message), "type": str(msg.message_type)}
            for msg in messages
        ]

        logger.info(f"📜 Historial guardado en state ({len(history_list)} mensajes).")
        return {"history_messages": history_list}

    except Exception as e:
        logger.error(f"❌ Error en get_history_tool: {e}")
        return {"history_messages": []}
