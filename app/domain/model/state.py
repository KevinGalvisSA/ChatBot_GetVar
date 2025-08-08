# app/domain/model/state.py

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
from app.models.context_chunk import ContextChunk

class State(BaseModel):
    # === Entrada del usuario ===
    input: Optional[str] = None  # Texto ingresado por el usuario

    # === Identificación y datos del usuario ===
    customer_id: Optional[int] = None
    session_id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None  # Cambiado a str por formatos internacionales
    company: Optional[str] = None
    rol: Optional[str] = None

    # === Estado del usuario y control interno ===
    user: bool = False
    user_saved: bool = False
    was_greeted: bool = False  # Evita repetir saludo

    # === Contexto recuperado del sistema de memoria o embeddings ===
    context: Optional[List[ContextChunk]] = None  # Lista de chunks relevantes

    # === Mensajes y flujo conversacional ===
    prompt: Optional[str] = None       # Prompt generado (si aplica)
    response: Optional[str] = None     # Respuesta generada para el usuario
    summary: Optional[str] = None      # Resumen del estado o conversación

    history_messages: Optional[List[Dict[str, str]]] = None
    # Ejemplo de mensaje: {"role": "user", "content": "¿Qué opciones tengo?"}

    # === Flags de control del flujo ===
    already_sent_solution: bool = False  # ¿Ya envió una solución (1, 2 o 3)?
    options_ab_sent: bool = False        # ¿Ya mostró opciones A y B?
    already_sent: bool = False           # ¿Ya respondió este paso?

    # === Timestamps para auditoría u orden cronológico ===
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
