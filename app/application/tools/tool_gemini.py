from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.factories.gemini_integration import answer_with_gemini
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CallGeminiInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=CallGeminiInput)
def call_gemini_tool(state: dict) -> dict:
    """
    Envía el prompt y el contexto a Gemini y devuelve la respuesta.
    """
    logger.info("\n🤖 [call_gemini_tool] Ejecutando tool...")

    # Extraemos el prompt y contexto (chunks) del estado
    prompt = state.get("prompt")
    if not prompt:
        logger.warning("⚠️ No se encontró 'prompt' en el estado.")
        prompt = "No prompt definido."

    chunks = state.get("context", [])
    # Aseguramos que chunks sea lista, aunque sea vacía
    if not isinstance(chunks, list):
        logger.warning("⚠️ 'context' no es lista, se ignora.")
        chunks = []

    try:
        result = answer_with_gemini(prompt, chunks)
        logger.info(f"✅ Respuesta recibida de Gemini:\n{result}\n")
    except Exception as e:
        result = "⚠️ Ocurrió un error al consultar Gemini."
        logger.error(f"❌ Error al llamar a Gemini: {e}")

    return {"response": result}
