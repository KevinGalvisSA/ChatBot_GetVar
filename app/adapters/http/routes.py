from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.application.agent.chatbot import chat_with_bot
from app.application.agent.chatbot import generate_chat_summary

router = APIRouter()

class UserInput(BaseModel):
    message: str
    session_id: str
    chat_id: int | None = None  # lo ignoramos

@router.post("/chat")
async def chat_with_bot_endpoint(user_input: UserInput):
    try:
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

@router.post("/resumen")
async def resumen_endpoint(user_input: UserInput):
    try:
        resumen = generate_chat_summary(session_id=user_input.session_id)
        return {"resumen": resumen}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"⚠️ Error al generar resumen: {str(e)}"
        )
