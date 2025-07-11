from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.infrastructure.langraph_orchestator import LangraphOrchestrator
from app.infrastructure.gemini_integration import answer_with_gemini
from app.infrastructure.qdrant import QdrantService
from app.models.context_chunk import ContextChunk
from config import Config  # Asegúrate de importar tu configuración

router = APIRouter()

# Inicializa el servicio de Qdrant
qdrant_service = QdrantService(
    url=Config.QDRANT_URL,
    collection_name=Config.QDRANT_COLLECTION_NAME,
    api_key=Config.QDRANT_API_KEY
)

# Inicializa el orquestador de Langraph
orchestrator = LangraphOrchestrator(
    qdrant_url=Config.QDRANT_URL,
    qdrant_collection_name=Config.QDRANT_COLLECTION_NAME,
    qdrant_api_key=Config.QDRANT_API_KEY
)

# Modelo de entrada del usuario
class UserInput(BaseModel):
    message: str  # El mensaje que el usuario enviará al bot

@router.post("/chat")
async def chat_with_bot_endpoint(user_input: UserInput):
    """
    Ruta que recibe una solicitud POST con el mensaje del usuario y
    devuelve la respuesta del chatbot, procesada a través de Qdrant y Gemini.
    """
    try:
        # Filtrar mensajes comunes como saludos
        greetings = ["hola", "buenas", "buenos días", "hey", "qué tal", "cómo estás"]
        if any(greeting in user_input.message.lower() for greeting in greetings):
            return {"response": "¡Hola! ¿Cómo puedo ayudarte hoy?"}
        
        print(f"🔍 Procesando mensaje: {user_input.message}")

        # Realizar la búsqueda explícita en Qdrant usando el servicio
        search_results = qdrant_service.search(user_input.message)

        if not search_results:
            return {"response": "Lo siento, no pude encontrar información relevante para tu consulta."}

        # Crear los fragmentos de contexto a partir de los resultados de búsqueda
        context_chunks = [ContextChunk(text=result, score=0.9) for result in search_results]  # type: ignore
        
        # Llamar a Gemini para generar la respuesta con el contexto y la pregunta
        response = answer_with_gemini(user_input.message, context_chunks)

        # Verificar si la respuesta generada por Gemini es válida
        if not response:
            raise HTTPException(status_code=400, detail="La respuesta del chatbot está vacía o mal formada.")

        return {"response": response}

    except Exception as e:
        # Si ocurre un error, devolver una excepción con el mensaje de error
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
