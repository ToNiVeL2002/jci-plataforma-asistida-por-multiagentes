"""
Modelos Pydantic para el módulo de Administrador
"""
from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):
    """
    Respuesta del dashboard del administrador con estadísticas globales
    """
    total_emprendedores: int
    total_mentores_activos: int
    diagnosticos_completados: int
    tasa_exito: float  # Porcentaje de diagnósticos ACEPTADO
    promedio_general: float
    promedio_cf: float
    promedio_gp: float
    promedio_m: float
    promedio_v: float
    promedio_tp: float
    promedio_rh: float
    
    class Config:
        from_attributes = True
