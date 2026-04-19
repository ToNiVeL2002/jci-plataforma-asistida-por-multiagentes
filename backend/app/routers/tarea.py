"""
Router para el módulo de Tareas
"""
from fastapi import APIRouter, Depends
from app.models.tarea import TareaCreate, TareaResponse
from app.services.tarea_service import tarea_service

router = APIRouter(prefix="/tarea", tags=["tarea"])


@router.post("", response_model=TareaResponse, status_code=201)
async def create_tarea(tarea_data: TareaCreate):
    """
    Crea una nueva tarea asignada a un emprendedor
    
    Args:
        tarea_data: Datos de la tarea (titulo, descripcion, fecha_expiracion, etc.)
    
    Returns:
        TareaResponse: Tarea creada con todos sus datos
    
    Raises:
        404: Si el usuario o diagnóstico no existe
        400: Si la validación falla (ej: fecha de expiración inválida)
        500: Si hay error al crear la tarea
    """
    return await tarea_service.create_tarea(tarea_data)
