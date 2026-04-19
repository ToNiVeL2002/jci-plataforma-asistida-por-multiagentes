"""
Router para el módulo de Administrador
"""
from fastapi import APIRouter, Depends
from app.models.admin import AdminDashboardResponse
from app.services.admin_service import admin_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard", response_model=AdminDashboardResponse)
async def get_admin_dashboard():
    """
    Obtiene las estadísticas globales para el dashboard del administrador
    
    Returns:
        AdminDashboardResponse: Estadísticas globales incluyendo:
        - Total de emprendedores
        - Total de mentores activos
        - Diagnósticos completados
        - Tasa de éxito
        - Promedios por área (CF, GP, M, V, TP, RH)
    """
    return await admin_service.get_dashboard_stats()
