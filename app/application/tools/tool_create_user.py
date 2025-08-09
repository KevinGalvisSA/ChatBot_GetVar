from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.sql.customer_saver import get_or_create_customer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreateUserInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=CreateUserInput)
def create_user_tool(state: dict) -> dict:
    """
    Crea un usuario en la base de datos si no existe, usando teléfono y nombre.
    """
    phone = state.get("phone")
    name = state.get("name")

    logger.info(f"[create_user] INICIO - phone='{phone}', name='{name}'")

    if not phone:
        logger.warning("⚠️ No se puede crear el usuario: falta teléfono.")
        return {"created": False, "customer_id": None, "message": "Falta teléfono"}

    customer = get_or_create_customer(name, phone)
    logger.info(f"[create_user] Cliente encontrado/creado: {customer}")

    return {
        "created": True,
        "customer_id": customer.id,
        "message": "Usuario creado o ya existente"
    }
