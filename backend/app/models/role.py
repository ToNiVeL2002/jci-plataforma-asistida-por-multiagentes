"""
Modelo para Roles de Usuario
"""
from pydantic import BaseModel
from typing import Optional


class Role(BaseModel):
    """
    Modelo de Rol
    Corresponde a la tabla 'rol' en Supabase
    """
    id_rol: int
    rol: str  # "Administrador", "Emprendedor", "Mentor"
    
    class Config:
        from_attributes = True
