
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.adapters.http.routes import router as chatbot_router

app = FastAPI()

# Manejo global de errores 422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "❌ Entrada inválida. Asegúrate de enviar 'session_id' y 'message'.",
            "detalles": exc.errors()
        },
    )

# Incluir rutas del bot
app.include_router(chatbot_router)