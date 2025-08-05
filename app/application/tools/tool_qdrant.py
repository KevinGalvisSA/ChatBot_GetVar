from app.domain.model.state import State
from app.infrastructure.factories.qdrant import QdrantService
from app.configuration import Config

# Instancia global del servicio Qdrant
qdrant = QdrantService(
    url=Config.QDRANT_URL,
    collection_name=Config.QDRANT_COLLECTION_NAME,
    api_key=Config.QDRANT_API_KEY
)

def retrieve_context_tool(state: State) -> dict:
    """
    Tool que busca contexto relacionado en Qdrant usando el input del usuario.
    """
    print("\n📚 [retrieve_context_tool] Buscando contexto similar en Qdrant...")

    query = state.input or ""
    print(f"🔎 Consulta recibida: '{query}'")

    context_chunks = []
    if not query.strip():
        print("⚠️ Consulta vacía. No se realizará búsqueda.")
    else:
        try:
            context_chunks = qdrant.search(query)
            print(f"✅ Contexto recuperado ({len(context_chunks)} chunks):")
            for idx, chunk in enumerate(context_chunks):
                print(f"  {idx + 1}. {chunk.text[:100]}... (score: {chunk.score:.4f})")
        except Exception as e:
            print(f"❌ Error al recuperar contexto de Qdrant: {e}")

    return {
        "context": context_chunks
    }
