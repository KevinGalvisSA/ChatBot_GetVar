from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """
    Modelo de datos del usuario que contiene solo los campos necesarios:
    - name: Nombre del usuario
    - phone_number: Teléfono del usuario
    """
    name: Optional[str] = None  # Nombre del usuario
    phone_number: Optional[str] = None  # Teléfono del usuario

    class Config:
        orm_mode = True  # Permite la conversión de modelos ORM si usamos una base de datos

    def __str__(self):
        return f"User(name={self.name}, phone_number={self.phone_number})"
