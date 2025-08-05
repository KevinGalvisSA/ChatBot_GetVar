from typing import Optional, List
from pydantic import BaseModel
from app.models.context_chunk import ContextChunk  # solo si estás usando contexto como lista

class State(BaseModel):
    # Entrada del usuario
    input: Optional[str] = None

    # Datos del usuario extraídos
    customer_id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    rol: Optional[str] = None

    # Control interno
    user: Optional[bool] = False
    user_saved: Optional[bool] = False

    # Contexto recuperado (mejor usar List[ContextChunk])
    context: Optional[List[ContextChunk]] = None  # <-- antes era str

    # Prompt generado y respuesta de Gemini
    prompt: Optional[str] = None
    response: Optional[str] = None
    summary: Optional[str] = None

    # Flags de control para condicionales
    already_sent_solution: Optional[bool] = False
    options_ab_sent: Optional[bool] = False
    already_sent: Optional[bool] = False  # <- este lo usas en el flujo
