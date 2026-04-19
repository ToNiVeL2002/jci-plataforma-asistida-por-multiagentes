"""
Modelos para Pregunta
"""
from pydantic import BaseModel
from typing import List


class PreguntaResponse(BaseModel):
    """
    Respuesta al obtener una pregunta
    """
    id_pregunta: int
    id_area: int
    enunciado: str
    
    class Config:
        from_attributes = True


class PreguntaConAreaResponse(BaseModel):
    """
    Pregunta con nombre del área incluido (para batch por área)
    """
    id_pregunta: int
    id_area: int
    nombre_area: str
    enunciado: str
    
    class Config:
        from_attributes = True


class AreaResponse(BaseModel):
    """
    Respuesta de un área
    """
    id_area: int
    nombre_area: str
    
    class Config:
        from_attributes = True
