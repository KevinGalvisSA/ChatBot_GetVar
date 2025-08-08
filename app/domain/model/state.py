# app/domain/model/state.py
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
from app.models.context_chunk import ContextChunk

class State(BaseModel):
    # Entrada del usuario
    input: Optional[str] = None

    # Datos del usuario extraídos
    customer_id: Optional[int] = None
    session_id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[int] = None
    company: Optional[str] = None
    rol: Optional[str] = None

    # Control interno
    user: Optional[bool] = False
    user_saved: Optional[bool] = False

    # Contexto recuperado
    context: Optional[List[ContextChunk]] = None

    # Prompt generado y respuesta
    prompt: Optional[str] = None
    response: Optional[str] = None
    summary: Optional[str] = None

    # Historial de mensajes
    history_messages: Optional[List[Dict[str, str]]] = None

    # Flags de control
    already_sent_solution: Optional[bool] = False
    options_ab_sent: Optional[bool] = False
    already_sent: Optional[bool] = False

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 
