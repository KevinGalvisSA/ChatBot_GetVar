# app/models/context_chunk.py
from pydantic import BaseModel

class ContextChunk(BaseModel):
    text: str
    score: float = 1.0
