# app/application/tools/tool_save_message.py

from app.infrastructure.sql.message_saver import get_messages_by_session, save_message
from app.domain.model.state import State

def save_message_tool(state: State, message_content: str, message_type: str) -> dict:
    """
    Guarda un mensaje nuevo en la BD y retorna el historial actualizado.
    """
    try:
        if not state.session_id or not state.customer_id:
            print("⚠️ No se proporcionó session_id o customer_id en el state.")
            return {"history_messages": state.history_messages or []}

        # Guardar el mensaje actual
        save_message(
            id_customer=state.customer_id,
            session_id=str(state.session_id),
            content=message_content,
            message_type=message_type
        )

        # Recargar historial actualizado (puedes limitar a 15)
        messages = get_messages_by_session(
            session_id=state.session_id,
            id_customer=state.customer_id,
            limit=15
        )

        history_list = [
            {"message": str(msg.message), "type": str(msg.message_type)}
            for msg in messages
        ]

        print(f"📜 Historial actualizado ({len(history_list)} mensajes).")
        return {"history_messages": history_list}

    except Exception as e:
        print(f"❌ Error en save_message_tool: {e}")
        return {"history_messages": state.history_messages or []}

def get_history_tool(state: State) -> dict:
    """
    Tool que obtiene los últimos 15 mensajes del historial para el cliente y sesión.
    Devuelve solo las actualizaciones para LangGraph.
    """
    try:
        if not state.session_id or not state.customer_id:
            print("⚠️ No se proporcionó session_id o customer_id en el state.")
            return {"history_messages": []}

        messages = get_messages_by_session(
            session_id=state.session_id,
            id_customer=state.customer_id,
            limit=15
        )

        history_list = [
            {"message": str(msg.message), "type": str(msg.message_type)}
            for msg in messages
        ]

        print(f"📜 Historial guardado en state ({len(history_list)} mensajes).")
        return {"history_messages": history_list}

    except Exception as e:
        print(f"❌ Error en get_history_tool: {e}")
        return {"history_messages": []}
