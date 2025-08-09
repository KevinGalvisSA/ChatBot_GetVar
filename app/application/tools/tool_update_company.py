from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.sql.customer_saver import update_customer_info, get_or_create_customer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StateInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=StateInput)
def update_company_tool(state: dict) -> dict:
    """
    Actualiza la empresa de un usuario usando los datos de state.
    Espera que el state tenga 'phone' y 'company'.
    """
    phone = state.get("phone")
    company = state.get("company")

    logger.info(f"[update_company] INICIO - phone='{phone}', company='{company}'")

    if not phone:
        logger.warning("⚠️ No se puede actualizar la empresa: falta teléfono.")
        return {"updated": False, "customer_id": None, "message": "Falta teléfono"}

    customer = get_or_create_customer(None, phone)
    if company and company != customer.company:
        update_customer_info(customer, company=company)
        logger.info("✅ Empresa actualizada correctamente")
        return {"updated": True, "customer_id": customer.id, "message": "Empresa actualizada"}

    logger.info("⚠️ No se detectaron cambios en la empresa")
    return {"updated": False, "customer_id": customer.id, "message": "No se detectaron cambios"}
