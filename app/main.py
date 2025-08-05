from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.adapters.http.routes import router as chatbot_router

app = FastAPI(
    title="Kai Bot API",
    description="API para gestionar las interacciones del bot vía FastAPI + LangGraph.",
    version="1.0.0"
)

# 📛 Manejo global de errores de validación (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "❌ Entrada inválida. Asegúrate de enviar los campos requeridos.",
            "detalles": exc.errors()
        },
    )

# 🚀 Rutas del chatbot (WhatsApp, Web, Telegram, etc.)
app.include_router(chatbot_router)
