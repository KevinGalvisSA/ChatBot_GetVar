from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.sql.customer_saver import update_customer_info, get_or_create_customer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StateInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=StateInput)
def update_role_tool(state: dict) -> dict:
    """
    Actualiza el rol/cargo de un usuario usando los datos del state.
    Espera que el state tenga 'phone' y 'rol'.
    """
    phone = state.get("phone")
    rol = state.get("rol")

    logger.info(f"[update_role] INICIO - phone='{phone}', rol='{rol}'")

    if not phone:
        logger.warning("⚠️ No se puede actualizar el rol: falta teléfono.")
        return {"updated": False, "customer_id": None, "message": "Falta teléfono"}

    customer = get_or_create_customer(None, phone)
    if rol and rol != customer.rol:
        update_customer_info(customer, rol=rol)
        logger.info("✅ Rol actualizado correctamente")
        return {"updated": True, "customer_id": customer.id, "message": "Rol actualizado"}

    logger.info("⚠️ No se detectaron cambios en el rol")
    return {"updated": False, "customer_id": customer.id, "message": "No se detectaron cambios"}
