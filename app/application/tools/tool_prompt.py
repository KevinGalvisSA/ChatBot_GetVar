from pydantic import BaseModel, Field, ValidationError
from langchain_core.tools import tool
from app.application.prompts.base_prompt import build_prompt
from app.domain.model.state import State
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BuildPromptInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool
def build_prompt_tool(state: dict) -> dict:
    """
    Genera el prompt completo uniendo el instructivo, resumen del usuario y el historial.
    """
    try:
        validated_input = BuildPromptInput(state=state)
        state_obj = State(**validated_input.state)
        prompt = build_prompt(state_obj)
        logger.info(f"✅ Prompt generado:\n{prompt}\n")
    except ValidationError as ve:
        prompt = "⚠️ Error de validación en la entrada."
        logger.error(f"❌ Validación fallida: {ve}")
    except Exception as e:
        prompt = "⚠️ Error al construir el prompt."
        logger.error(f"❌ Error en build_prompt: {e}")

    return {"prompt": prompt}
