from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.sql.customer_saver import update_customer_info, get_or_create_customer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StateInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=StateInput)
def update_name_tool(state: dict) -> dict:
    """
    Actualiza el nombre de un usuario usando los datos de state.
    Espera que el state tenga 'phone' y 'name'.
    """
    phone = state.get("phone")
    name = state.get("name")

    logger.info(f"[update_name] INICIO - phone='{phone}', name='{name}'")

    if not phone:
        logger.warning("⚠️ No se puede actualizar el nombre: falta teléfono.")
        return {"updated": False, "customer_id": None, "message": "Falta teléfono"}

    customer = get_or_create_customer(None, phone)
    if name and name != customer.name:
        update_customer_info(customer, name=name)
        logger.info("✅ Nombre actualizado correctamente")
        return {"updated": True, "customer_id": customer.id, "message": "Nombre actualizado"}

    logger.info("⚠️ No se detectaron cambios en el nombre")
    return {"updated": False, "customer_id": customer.id, "message": "No se detectaron cambios"}
