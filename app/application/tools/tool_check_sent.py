import re
import logging
from pydantic import BaseModel, Field
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CheckAlreadySentInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=CheckAlreadySentInput)
def check_already_sent_tool(state: dict) -> dict:
    """
    Revisa si la solución ya fue enviada previamente.
    Busca 'solucion a' o 'solucion b' en el texto de respuesta.
    """
    logger.info("\n📌 [check_already_sent_tool] Ejecutando tool...")

    response_text = (state.get("response") or "").lower().replace("ó", "o")

    contiene_a = bool(re.search(r'\bsolucion a\b', response_text))
    contiene_b = bool(re.search(r'\bsolucion b\b', response_text))

    logger.info(f"🔍 ¿Contiene 'solucion a'? ➜ {contiene_a}")
    logger.info(f"🔍 ¿Contiene 'solucion b'? ➜ {contiene_b}")

    already_sent = contiene_a or contiene_b
    logger.info(f"📤 [check_already_sent_tool] Resultado ➜ already_sent_solution: {already_sent}\n")

    return {"already_sent_solution": already_sent}
