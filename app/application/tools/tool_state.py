# app/application/tools/tool_state.py

import datetime
from langchain_core.tools import tool
from app.domain.model.state import State
from app.infrastructure.sql.state_saver import StateSaver


def is_greeting(message: str) -> bool:
    """Detecta si un mensaje es un saludo."""
    if not message:
        return False
    greetings = ["hola", "buenas", "qué tal", "hello", "hi"]
    message_lower = message.strip().lower()
    return any(message_lower.startswith(g) for g in greetings)


def save_state_tool(state: dict) -> dict:
    """
    Guarda o actualiza el State en la base de datos.
    Si es un saludo después de un tiempo prolongado, resetea flags de control.
    """
    session_id = state.get("session_id")
    if session_id is None:
        raise ValueError("❌ No se puede guardar el state: session_id es None")

    existing_state = StateSaver.get_by_session(session_id)

    if existing_state:
        # Verificamos si corresponde resetear
        if is_greeting(str(state.get("input"))):
            last_update = getattr(existing_state, "updated_at", None)
            if isinstance(last_update, datetime.datetime):
                if datetime.datetime.utcnow() - last_update > datetime.timedelta(minutes=30):
                    state["already_sent_solution"] = False
                    state["options_ab_sent"] = False
                    state["already_sent"] = False
                    state["context"] = None
                    state["prompt"] = None
                    state["response"] = None
                    state["summary"] = None

        StateSaver.update_state(session_id, State(**state))
        return {"message": f"🔄 State actualizado para session_id={session_id}"}
    else:
        StateSaver.save_state(State(**state))
        return {"message": f"✅ State creado para session_id={session_id}"}



def get_state_tool(session_id: int) -> dict:
    """
    Obtiene el State de la base de datos para un session_id.
    Si no existe, retorna un state vacío como dict.
    """
    if session_id is None:
        raise ValueError("❌ No se puede obtener el state: session_id es None")

    existing_state = StateSaver.get_by_session(session_id)

    if existing_state:
        # Convierte el modelo de la BD en dict (ignorando atributos internos como _sa_instance_state)
        state_dict = {
            k: v
            for k, v in existing_state.__dict__.items()
            if not k.startswith("_")
        }
        return state_dict

    # Si no existe, devolvemos uno inicial
    empty_state = State(
        session_id=session_id,
        name=None,
        phone=None,
        company=None,
        rol=None,
        input=None,
        context=None,
        prompt=None,
        response=None,
        summary=None,
        already_sent_solution=False,
        options_ab_sent=False,
        already_sent=False
    )
    return empty_state.__dict__


def delete_state_tool(session_id: int) -> dict:
    """
    Elimina el State de la base de datos para un session_id.
    Retorna un dict con confirmación.
    """
    if session_id is None:
        raise ValueError("❌ No se puede eliminar el state: session_id es None")

    deleted = StateSaver.delete_state(session_id)
    return {
        "session_id": session_id,
        "deleted": bool(deleted),
        "message": "🗑️ State eliminado" if deleted else "⚠️ No se encontró state para eliminar"
    }
