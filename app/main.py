from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from app.infrastructure.langGraph_orchestrator import LangraphOrchestrator  # Importa el orquestador de LangGraph
from app.infrastructure.qdrant import QdrantService
from app.configEnv import Config
from app.application.chatbot import capture_user_data  # Función de captura de datos del usuario

# Inicializa FastAPI
app = FastAPI(title="Chatbot Asesor")

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

# Define el enrutador de la API
router = APIRouter()

# Modelo de entrada del usuario
class UserInput(BaseModel):
    message: str  # El mensaje que el usuario enviará al bot

@app.get("/")
async def read_root():
    """
    Endpoint de prueba para asegurarse de que la API está corriendo correctamente.
    """
    return {"message": "Bienvenido al Chatbot Asesor"}

# Función de captura de datos del usuario
@router.post("/chat")
async def chat_with_bot_endpoint(user_input: UserInput):
    try:
        print(f"Recibiendo mensaje del usuario: {user_input.message}")  # Log para verificar que FastAPI está recibiendo el mensaje

        # Intentar capturar datos del usuario (por ejemplo, nombre, teléfono, etc.)
        capture_user_data(user_input.message)

        # Generar respuesta usando LangGraph, que procesará con Gemini
        response = orchestrator.run(user_input.message)  # Llama al orquestador de LangGraph
        print(f"Respuesta generada por el chatbot: {response}")  # Verificar la respuesta

        return {"response": response}

    except Exception as e:
        print(f"Error al procesar la solicitud: {str(e)}")  # Log si hay error
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

# Agregar el enrutador al servidor FastAPI
app.include_router(router)

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """
    Función de inicio del servicio para inicializar conexiones o servicios, si es necesario.
    """
    print("🚀 El servidor de FastAPI está iniciando...")

# Evento de apagado
@app.on_event("shutdown")
async def shutdown_event():
    """
    Función de apagado para cerrar cualquier recurso o conexión, si es necesario.
    """
    print("🛑 El servidor de FastAPI se está apagando...")

# Iniciar main.py
# uvicorn app.main:app --reload
