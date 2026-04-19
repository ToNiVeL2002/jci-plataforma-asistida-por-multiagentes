"""
Modelos para Diagnóstico
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DiagnosticoCreate(BaseModel):
    """
    Modelo para crear un nuevo diagnóstico
    Solo requiere id_usuario, los demás campos se inicializan automáticamente
    """
    id_usuario: str


class DiagnosticoResponse(BaseModel):
    """
    Respuesta al crear un diagnóstico
    """
    id_diagnostico: int
    id_usuario: str
    fecha_inicio: datetime
    puntaje_total: Optional[Decimal] = None
    conclusion: Optional[str] = None
    resultado: Optional[str] = None
    puntaje_cf: Optional[Decimal] = None
    puntaje_gp: Optional[Decimal] = None
    puntaje_m: Optional[Decimal] = None
    puntaje_v: Optional[Decimal] = None
    puntaje_tp: Optional[Decimal] = None
    puntaje_rh: Optional[Decimal] = None
    puntaje_ec: Optional[Decimal] = None
    recomendaciones: Optional[str] = None
    inconsistencias: Optional[str] = None
    
    class Config:
        from_attributes = True


class DetalleDiagnosticoCreate(BaseModel):
    """
    Modelo para crear un detalle de diagnóstico (respuesta a una pregunta)
    """
    id_diagnostico: int
    id_pregunta: int
    respuesta_usuario: str
    puntaje: float  # Cambiar de Decimal a float


class DetalleDiagnosticoResponse(BaseModel):
    """
    Respuesta al crear un detalle de diagnóstico
    """
    id_detalle: int
    id_diagnostico: int
    id_pregunta: int
    respuesta_usuario: str
    puntaje: float  # Cambiar de Decimal a float para serialización JSON
    
    class Config:
        from_attributes = True


class DiagnosticoUpdate(BaseModel):
    """
    Modelo para actualizar un diagnóstico con los resultados finales
    """
    puntaje_total: Decimal
    conclusion: str
    resultado: str
    puntaje_cf: Decimal
    puntaje_gp: Decimal
    puntaje_m: Decimal
    puntaje_v: Decimal
    puntaje_tp: Decimal
    puntaje_rh: Decimal
    puntaje_ec: Decimal
    recomendaciones: Optional[str] = None
    inconsistencias: Optional[str] = None


# ============ Modelos para IA ============

class IniciarDiagnosticoIARequest(BaseModel):
    """
    Request para iniciar una sesión de diagnóstico con la IA
    """
    id_usuario: str
    nombre_usuario: str
    nombre_emprendimiento: Optional[str] = None
    rubro: Optional[str] = None
    anio_inicio: Optional[int] = None
    numero_personal: Optional[int] = None
    ventas_men_prom: Optional[float] = None


class AreaInfo(BaseModel):
    id_area: int
    nombre_area: str


class IniciarDiagnosticoIAResponse(BaseModel):
    """
    Response al iniciar sesión con la IA (incluye áreas y diagnóstico creado)
    """
    session_id: str
    user_id: str
    id_diagnostico: int
    areas: list[AreaInfo]
    mensaje_inicial: str


class ChatIARequest(BaseModel):
    session_id: str
    user_id: str
    mensaje: str


class ChatIAResponse(BaseModel):
    respuesta: str


# ============ Modelos para IA Batch (por área) ============

class PreguntaReformulada(BaseModel):
    id_pregunta: int
    area: str
    intro: str
    pregunta: str
    ejemplo: str


class PreguntasAreaRequest(BaseModel):
    session_id: str
    user_id: str
    id_area: int


class PreguntasAreaResponse(BaseModel):
    id_area: int
    nombre_area: str
    preguntas: list[PreguntaReformulada]


class RespuestaUsuario(BaseModel):
    id_pregunta: int
    respuesta: str


class ScorePregunta(BaseModel):
    id_pregunta: int
    score: int
    reason: str


class EvaluarAreaRequest(BaseModel):
    session_id: str
    user_id: str
    id_area: int
    respuestas: list[RespuestaUsuario]


class EvaluarAreaResponse(BaseModel):
    scores: list[ScorePregunta]
    area_promedio: float
    inconsistencias: list[str]


class ResultadosRequest(BaseModel):
    session_id: str
    user_id: str
    area_scores: list[dict] = []   # [{"id_area": 1, "area_promedio": 72.5}, ...]


class ResultadosResponse(BaseModel):
    mensaje_despedida: str
    puntaje_total: float
