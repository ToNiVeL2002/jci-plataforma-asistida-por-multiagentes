"""
Modelo para actualización de datos de usuario
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserUpdateRequest(BaseModel):
    """
    Modelo para actualizar datos personales del usuario
    """
    nombre: str
    apellido: str
    sexo: str  # "M", "F", "O"
    fecha_nacimiento: date
    celular: int
