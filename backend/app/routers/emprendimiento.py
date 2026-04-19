"""
Router de Emprendimiento
Endpoints para gestión de emprendimientos y sus estados
"""
from fastapi import APIRouter, HTTPException, status
from app.services.emprendimiento_service import EmprendimientoService
from app.models.emprendimiento import (
    CreateEmprendimientoRequest,
    EmprendimientoResponse,
    CreateEstadoEmprendimientoRequest,
    EstadoEmprendimientoResponse
)


router = APIRouter(prefix="/emprendimiento", tags=["Emprendimiento"])


@router.post("", response_model=EmprendimientoResponse, status_code=status.HTTP_201_CREATED)
async def create_emprendimiento(emprendimiento_data: CreateEmprendimientoRequest):
    """
    Crea un nuevo emprendimiento para un usuario

    Args:
        emprendimiento_data: Datos del emprendimiento (id_usuario, nombre, rubro, anio_inicio)

    Returns:
        EmprendimientoResponse: Emprendimiento creado

    Raises:
        400: Si el usuario ya tiene un emprendimiento
        500: Error interno del servidor
    """
    emprendimiento_service = EmprendimientoService()

    try:
        emprendimiento = await emprendimiento_service.create_emprendimiento(emprendimiento_data)
        return emprendimiento

    except Exception as e:
        error_message = str(e)
        if "ya tiene un emprendimiento" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear emprendimiento: {error_message}"
        )


@router.get("/usuario/{id_usuario}", response_model=EmprendimientoResponse | None)
async def get_emprendimiento_by_user(id_usuario: str):
    """
    Obtiene el emprendimiento de un usuario

    Args:
        id_usuario: ID del usuario

    Returns:
        EmprendimientoResponse | None: Emprendimiento del usuario o null si no existe

    Raises:
        500: Error interno del servidor
    """
    emprendimiento_service = EmprendimientoService()

    try:
        emprendimiento = await emprendimiento_service.get_emprendimiento_by_user(id_usuario)
        return emprendimiento

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener emprendimiento: {str(e)}"
        )


@router.post("/estado", response_model=EstadoEmprendimientoResponse, status_code=status.HTTP_201_CREATED)
async def create_estado_emprendimiento(estado_data: CreateEstadoEmprendimientoRequest):
    """
    Crea un nuevo registro de estado del emprendimiento
    Se crea cada vez que el usuario entra al diagnóstico con IA

    Args:
        estado_data: Datos del estado (id_emprendimiento, numero_personal, ventas_men_prom)

    Returns:
        EstadoEmprendimientoResponse: Estado del emprendimiento creado

    Raises:
        500: Error interno del servidor
    """
    emprendimiento_service = EmprendimientoService()

    try:
        estado = await emprendimiento_service.create_estado_emprendimiento(estado_data)
        return estado

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear estado del emprendimiento: {str(e)}"
        )


@router.get("/{id_emprendimiento}/estados", response_model=list[EstadoEmprendimientoResponse])
async def get_estados_emprendimiento(id_emprendimiento: int):
    """
    Obtiene el historial de estados de un emprendimiento

    Args:
        id_emprendimiento: ID del emprendimiento

    Returns:
        list[EstadoEmprendimientoResponse]: Lista de estados ordenados por fecha (más reciente primero)

    Raises:
        500: Error interno del servidor
    """
    emprendimiento_service = EmprendimientoService()

    try:
        estados = await emprendimiento_service.get_estado_emprendimiento_by_id(id_emprendimiento)
        return estados

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estados del emprendimiento: {str(e)}"
        )
