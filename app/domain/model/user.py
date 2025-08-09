from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """
    Modelo de datos del usuario que contiene solo los campos necesarios:
    - name: Nombre del usuario
    - phone: Teléfono del usuario
    """
    name: Optional[str] = None
    phone: Optional[int] = None

    class Config:
        orm_mode = True  # Permite la conversión desde modelos ORM (como SQLAlchemy)

    def __str__(self):
        return f"User(name={self.name}, phone={self.phone})"
