# app/application/tools/tool_extract_info.py

from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.factories.extract_info import InfoExtractor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractUserInfoInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=ExtractUserInfoInput)
def extract_user_info_tool(state: dict) -> dict:
    """
    Extrae información como nombre, teléfono, rol y empresa
    del mensaje actual del usuario, usando InfoExtractor.
    Retorna los datos encontrados para actualizar el state.
    """
    logger.info("\n📌 [extract_user_info_tool] Ejecutando tool...")
    try:
        user_text = state.get("input")
        logger.info(f"🔍 Texto del usuario: {user_text}")
        if not user_text:
            logger.warning("⚠️ No se encontró texto en state['input']")
            return {
                "name": None,
                "phone": None,
                "company": None,
                "rol": None
            }

        extractor = InfoExtractor()
        extracted_info = extractor.extract(user_text)

        logger.info(f"🔍 Información extraída: {extracted_info}")
        return extracted_info

    except Exception as e:
        logger.error(f"❌ Error en extract_user_info_tool: {e}")
        return {
            "name": None,
            "phone": None,
            "company": None,
            "rol": None
        }
