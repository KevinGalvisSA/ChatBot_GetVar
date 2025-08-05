# app/adapters/http/routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.application.agent.chatbot import chat_with_bot, generate_chat_summary
import traceback

router = APIRouter()

class UserInput(BaseModel):
    message: str
    session_id: str
    chat_id: int | None = None  # Ignorado de momento

@router.post("/chat")
async def chat_with_bot_endpoint(user_input: UserInput):
    try:
        response = await chat_with_bot(
            user_input=user_input.message,
            session_id=user_input.session_id
        )
        return {"response": response}
    except Exception as e:
        print("❌ Excepción capturada en /chat:")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"⚠️ Error al procesar el mensaje: {str(e)}"
        )

@router.post("/resumen")
async def resumen_endpoint(user_input: UserInput):
    """
    Endpoint para generar el resumen de la conversación.
    """
    try:
        resumen = generate_chat_summary(session_id=user_input.session_id)
        return {"resumen": resumen}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"⚠️ Error al generar el resumen: {str(e)}"
        )
