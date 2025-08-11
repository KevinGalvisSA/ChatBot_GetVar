# app/application/tools/tool_state.py

import datetime
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.domain.model.state import State
from app.infrastructure.sql.state_saver import StateSaver


class StateInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")


def is_greeting(message: str) -> bool:
    """Detecta si un mensaje es un saludo."""
    if not message:
        return False
    greetings = ["hola", "buenas", "qué tal", "hello", "hi"]
    message_lower = message.strip().lower()
    return any(message_lower.startswith(g) for g in greetings)


@tool(args_schema=StateInput)
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
        if is_greeting(str(state.get("input"))):
            last_update = getattr(existing_state, "updated_at", None)
            if isinstance(last_update, datetime.datetime):
                if datetime.datetime.utcnow() - last_update > datetime.timedelta(minutes=30):
                    state.update({
                        "already_sent_solution": False,
                        "options_ab_sent": False,
                        "already_sent": False,
                        "context": None,
                        "prompt": None,
                        "response": None,
                        "summary": None
                    })

        StateSaver.update_state(session_id, State(**state))
        return {"message": f"🔄 State actualizado para session_id={session_id}"}

    StateSaver.save_state(State(**state))
    return {"message": f"✅ State creado para session_id={session_id}"}


@tool(args_schema=StateInput)
def get_state_tool(state: dict) -> dict:
    """
    Obtiene el State de la base de datos para un session_id.
    Actualiza el state recibido con los datos de la base (old_data),
    solo para campos que en old_data no sean None y que falten o sean None en state.
    """
    session_id = state.get("session_id")
    if session_id is None:
        raise ValueError("❌ No se puede obtener el state: session_id es None")

    old_data_obj = StateSaver.get_by_session(session_id)
    if old_data_obj:
        old_data = {
            k: v
            for k, v in old_data_obj.__dict__.items()
            if not k.startswith("_")
        }
    else:
        old_data = State(session_id=session_id).model_dump()

    # Actualizar el state recibido con los valores de old_data que no sean None
    updated_state = state.copy()
    for key, value in old_data.items():
        if value is not None and (updated_state.get(key) is None):
            updated_state[key] = value

    return updated_state


@tool(args_schema=StateInput)
def delete_state_tool(state: dict) -> dict:
    """
    Elimina el State de la base de datos para un session_id.
    Retorna un dict con confirmación.
    """
    session_id = state.get("session_id")
    if session_id is None:
        raise ValueError("❌ No se puede eliminar el state: session_id es None")

    deleted = StateSaver.delete_state(session_id)
    return {
        "session_id": session_id,
        "deleted": bool(deleted),
        "message": "🗑️ State eliminado" if deleted else "⚠️ No se encontró state para eliminar"
    }
