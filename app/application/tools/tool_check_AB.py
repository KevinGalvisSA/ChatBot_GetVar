import re
import logging
from pydantic import BaseModel, Field
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CheckABInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=CheckABInput)
def check_AB_tool(state: dict) -> dict:
    """
    Evalúa si el bot ya ofreció las opciones A y B (venta o capacitación).
    Busca 'opcion a' o 'opcion b' en el texto de respuesta.
    """
    logger.info("\n📌 [check_AB_tool] Ejecutando tool...")

    response_text = (state.get("response") or "").lower().replace("ó", "o")

    contiene_a = bool(re.search(r'\bopcion a\b', response_text))
    contiene_b = bool(re.search(r'\bopcion b\b', response_text))

    logger.info(f"🔍 ¿Contiene 'opcion a'? ➜ {contiene_a}")
    logger.info(f"🔍 ¿Contiene 'opcion b'? ➜ {contiene_b}")

    options_ab_sent = contiene_a or contiene_b
    logger.info(f"📤 [check_AB_tool] Resultado ➜ options_ab_sent: {options_ab_sent}\n")

    return {"options_ab_sent": options_ab_sent}
