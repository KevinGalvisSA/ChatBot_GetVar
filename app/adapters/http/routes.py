from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.infrastructure.langGraph_orchestrator import LangraphOrchestrator  # Importa el orquestador de LangGraph
from app.configEnv import Config
from app.infrastructure.qdrant import QdrantService
from app.application.chatbot import capture_user_data

router = APIRouter()

# Inicializa el servicio de Qdrant
qdrant_service = QdrantService(
    url=Config.QDRANT_URL,
    collection_name=Config.QDRANT_COLLECTION_NAME,
    api_key=Config.QDRANT_API_KEY
)

# Inicializa el orquestador de LangGraph
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
    try:
        # Intentar capturar datos del usuario (por ejemplo, nombre, teléfono, etc.)
        capture_user_data(user_input.message)

        # Generar respuesta usando LangGraph, que procesará con Gemini
        response = orchestrator.run(user_input.message)  # Llama al orquestador de LangGraph

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
