from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.infrastructure.langraph_orchestator import LangraphOrchestrator
from app.infrastructure.qdrant import QdrantService
from config import Config
from app.application.chatbot import chat_with_bot, capture_user_data

router = APIRouter()

# Inicializa el servicio de Qdrant
qdrant_service = QdrantService(
    url=Config.QDRANT_URL,
    collection_name=Config.QDRANT_COLLECTION_NAME,
    api_key=Config.QDRANT_API_KEY
)

# Inicializa el orquestador de Langgraph
orchestrator = LangraphOrchestrator(
    qdrant_url=Config.QDRANT_URL,
    qdrant_collection_name=Config.QDRANT_COLLECTION_NAME,
    qdrant_api_key=Config.QDRANT_API_KEY
)

# Modelo de entrada del usuario con session_id y mensaje
class UserInput(BaseModel):
    session_id: str  # Identificador único de la sesión o usuario
    message: str     # Mensaje enviado por el usuario

@router.post("/chat")
async def chat_with_bot_endpoint(user_input: UserInput):
    """
    Endpoint principal del chatbot.

    - Captura datos del usuario si se encuentran en el mensaje.
    - Usa LangGraph y Gemini para generar una respuesta.
    - Guarda el historial usando `session_id` para persistencia.
    """
    try:
        # Captura automática (si aplica)
        capture_user_data(user_input.message)

        # Conversación con el bot, usando memoria persistente
        response = chat_with_bot(user_input.message, user_input.session_id)

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
