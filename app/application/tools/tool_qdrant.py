from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.infrastructure.factories.qdrant import QdrantService
from app.configuration import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instancia global del servicio Qdrant
qdrant = QdrantService(
    url=Config.QDRANT_URL,
    collection_name=Config.QDRANT_COLLECTION_NAME,
    api_key=Config.QDRANT_API_KEY  # type: ignore
)

class RetrieveContextInput(BaseModel):
    state: dict = Field(description="Estado completo de la sesión como diccionario")

@tool(args_schema=RetrieveContextInput)
def retrieve_context_tool(state: dict) -> dict:
    """
    Busca contexto relacionado en Qdrant usando el input del usuario.
    """
    logger.info("\n📚 [retrieve_context_tool] Buscando contexto similar en Qdrant...")

    query = state.get("input", "") or ""
    logger.info(f"🔎 Consulta recibida: '{query}'")

    context_chunks = []
    if not query.strip():
        logger.warning("⚠️ Consulta vacía. No se realizará búsqueda.")
    else:
        try:
            context_chunks = qdrant.search(query)
            logger.info(f"✅ Contexto recuperado ({len(context_chunks)} chunks):")
            for idx, chunk in enumerate(context_chunks):
                logger.info(f"  {idx + 1}. {chunk.text[:100]}... (score: {chunk.score:.4f})")
        except Exception as e:
            logger.error(f"❌ Error al recuperar contexto de Qdrant: {e}")

    return {"context": context_chunks}
