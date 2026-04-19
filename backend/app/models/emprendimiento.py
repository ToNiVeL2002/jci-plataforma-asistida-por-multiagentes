"""
Modelos Pydantic para Emprendimiento y Estado de Emprendimiento
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Rubro(str, Enum):
    """Tipos de rubro para emprendimientos"""
    COMERCIO_VENTAS = "Comercio y Ventas"
    GASTRONOMIA = "Gastronomía"
    SERVICIOS_PERSONALES = "Servicios Personales"
    ARTES_MANUALIDADES = "Artes y Manualidades"
    TECNOLOGIA_EDUCACION = "Tecnología y Educación"
    AGRO_PRODUCCION = "Agro y Producción"
    OTROS = "Otros"


class CreateEmprendimientoRequest(BaseModel):
    """Request para crear un emprendimiento"""
    id_usuario: str
    nombre: str = Field(..., min_length=1, description="Nombre del emprendimiento")
    rubro: Rubro = Field(..., description="Rubro del emprendimiento")
    anio_inicio: int = Field(..., ge=1900, le=2100, description="Año de inicio del emprendimiento")


class EmprendimientoResponse(BaseModel):
    """Response con datos del emprendimiento"""
    id_emprendimiento: int
    id_usuario: str
    nombre: str
    rubro: str
    anio_inicio: int
    created_at: datetime

    class Config:
        from_attributes = True


class CreateEstadoEmprendimientoRequest(BaseModel):
    """Request para crear estado del emprendimiento"""
    id_emprendimiento: int
    numero_personal: int = Field(..., ge=0, description="Número de personas en el emprendimiento")
    ventas_men_prom: float = Field(..., ge=0, description="Ventas mensuales promedio")


class EstadoEmprendimientoResponse(BaseModel):
    """Response con datos del estado del emprendimiento"""
    id_estado_emp: int
    id_emprendimiento: int
    numero_personal: int
    ventas_men_prom: float
    fecha_registro_estado: datetime

    class Config:
        from_attributes = True
