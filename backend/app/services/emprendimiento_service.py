"""
Servicio de Emprendimiento
Maneja operaciones CRUD para emprendimientos y sus estados
"""
from typing import Optional
from app.services.supabase_client import get_supabase_client
from app.models.emprendimiento import (
    CreateEmprendimientoRequest,
    EmprendimientoResponse,
    CreateEstadoEmprendimientoRequest,
    EstadoEmprendimientoResponse
)


class EmprendimientoService:
    """Servicio para gestión de emprendimientos"""

    def __init__(self):
        """Inicializa el servicio con el cliente de Supabase"""
        self.supabase = get_supabase_client()

    async def create_emprendimiento(self, emprendimiento_data: CreateEmprendimientoRequest) -> EmprendimientoResponse:
        """
        Crea un nuevo emprendimiento

        Args:
            emprendimiento_data: Datos del emprendimiento a crear

        Returns:
            EmprendimientoResponse: Emprendimiento creado

        Raises:
            Exception: Si hay error en la creación o si el usuario ya tiene un emprendimiento
        """
        # Verificar que el usuario no tenga ya un emprendimiento
        existing = await self.get_emprendimiento_by_user(emprendimiento_data.id_usuario)
        if existing:
            raise Exception("El usuario ya tiene un emprendimiento registrado")

        # Preparar datos para insertar
        insert_data = {
            "id_usuario": emprendimiento_data.id_usuario,
            "nombre": emprendimiento_data.nombre,
            "rubro": emprendimiento_data.rubro.value,  # Obtener el valor del enum
            "anio_inicio": emprendimiento_data.anio_inicio
        }

        # Insertar en Supabase
        result = self.supabase.table("emprendimiento").insert(insert_data).execute()

        if not result.data:
            raise Exception("Error al crear emprendimiento en la base de datos")

        return EmprendimientoResponse(**result.data[0])

    async def get_emprendimiento_by_user(self, id_usuario: str) -> Optional[EmprendimientoResponse]:
        """
        Obtiene el emprendimiento de un usuario

        Args:
            id_usuario: ID del usuario

        Returns:
            EmprendimientoResponse | None: Emprendimiento del usuario o None si no existe
        """
        result = self.supabase.table("emprendimiento").select("*").eq("id_usuario", id_usuario).execute()

        if not result.data:
            return None

        return EmprendimientoResponse(**result.data[0])

    async def create_estado_emprendimiento(
        self, 
        estado_data: CreateEstadoEmprendimientoRequest
    ) -> EstadoEmprendimientoResponse:
        """
        Crea un nuevo registro de estado del emprendimiento

        Args:
            estado_data: Datos del estado a registrar

        Returns:
            EstadoEmprendimientoResponse: Estado del emprendimiento creado

        Raises:
            Exception: Si hay error en la creación
        """
        # Preparar datos para insertar
        insert_data = {
            "id_emprendimiento": estado_data.id_emprendimiento,
            "numero_personal": estado_data.numero_personal,
            "ventas_men_prom": estado_data.ventas_men_prom
        }

        # Insertar en Supabase
        result = self.supabase.table("estado_emprendimiento").insert(insert_data).execute()

        if not result.data:
            raise Exception("Error al crear estado del emprendimiento en la base de datos")

        return EstadoEmprendimientoResponse(**result.data[0])

    async def get_estado_emprendimiento_by_id(self, id_emprendimiento: int) -> list[EstadoEmprendimientoResponse]:
        """
        Obtiene todos los estados de un emprendimiento

        Args:
            id_emprendimiento: ID del emprendimiento

        Returns:
            list[EstadoEmprendimientoResponse]: Lista de estados del emprendimiento
        """
        result = self.supabase.table("estado_emprendimiento").select("*").eq(
            "id_emprendimiento", id_emprendimiento
        ).order("fecha_registro_estado", desc=True).execute()

        return [EstadoEmprendimientoResponse(**item) for item in result.data]
