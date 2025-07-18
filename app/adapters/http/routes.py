# app/adapters/http/routes.py

from fastapi import APIRouter, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.infrastructure.factories.langraph_orchestator import LangraphOrchestrator
from app.infrastructure.factories.qdrant import QdrantService
from config import Config 
from app.application.agent.chatbot import chat_with_bot, capture_user_data

router = APIRouter()

# Inicializa servicios externos
qdrant_service = QdrantService(
    url=Config.QDRANT_URL,
    collection_name=Config.QDRANT_COLLECTION_NAME,
    api_key=Config.QDRANT_API_KEY
)

orchestrator = LangraphOrchestrator(
    qdrant_url=Config.QDRANT_URL,
    qdrant_collection_name=Config.QDRANT_COLLECTION_NAME,
    qdrant_api_key=Config.QDRANT_API_KEY
)

# Modelo que se espera recibir en la petición POST
class UserInput(BaseModel):
    message: str
    session_id: str


# Manejador de errores personalizados para 422
# @router.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content={
#             "error": "❌ Datos de entrada inválidos. Asegúrate de enviar 'session_id' y 'message'.",
#             "detalles": exc.errors()
#         },
#     )

# Endpoint para interactuar con el bot
@router.post("/chat")
async def chat_with_bot_endpoint(user_input: UserInput):
    try:
        capture_user_data(user_input.message)  # si esto aplica a tu lógica

        response = chat_with_bot(
            user_input=user_input.message,
            session_id=user_input.session_id
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"⚠️ Error al procesar la solicitud: {str(e)}"
        )
