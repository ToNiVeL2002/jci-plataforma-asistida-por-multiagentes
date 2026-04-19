"""
Servicio de Tareas
Maneja la lógica de negocio para gestión de tareas
"""
from typing import Optional
from fastapi import HTTPException, status
from app.services.supabase_client import get_supabase_client
from app.models.tarea import TareaCreate, TareaResponse


class TareaService:
    """Servicio para manejar tareas"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def create_tarea(self, tarea_data: TareaCreate) -> TareaResponse:
        """
        Crea una nueva tarea
        
        Args:
            tarea_data: Datos de la tarea a crear
        
        Returns:
            TareaResponse: Tarea creada
        
        Raises:
            HTTPException: Si hay error al crear la tarea
        """
        try:
            # 1. Validar que el usuario existe
            user_response = self.supabase.table("usuario") \
                .select("id_usuario") \
                .eq("id_usuario", tarea_data.id_usuario) \
                .execute()
            
            if not user_response.data or len(user_response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con ID {tarea_data.id_usuario} no encontrado"
                )
            
            # 2. Validar que el diagnóstico existe
            diagnostico_response = self.supabase.table("diagnostico") \
                .select("id_diagnostico") \
                .eq("id_diagnostico", tarea_data.id_diagnostico) \
                .execute()
            
            if not diagnostico_response.data or len(diagnostico_response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Diagnóstico con ID {tarea_data.id_diagnostico} no encontrado"
                )
            
            # 3. Crear la tarea
            tarea_insert = {
                "id_usuario": tarea_data.id_usuario,
                "id_diagnostico": tarea_data.id_diagnostico,
                "titulo": tarea_data.titulo,
                "descripcion": tarea_data.descripcion,
                "fecha_expiracion": tarea_data.fecha_expiracion.isoformat(),
                "estado": "Pendiente"
            }
            
            response = self.supabase.table("tarea") \
                .insert(tarea_insert) \
                .execute()
            
            if not response.data or len(response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear la tarea"
                )
            
            tarea_created = response.data[0]
            
            return TareaResponse(
                id_tarea=tarea_created["id_tarea"],
                id_usuario=tarea_created["id_usuario"],
                id_diagnostico=tarea_created["id_diagnostico"],
                titulo=tarea_created["titulo"],
                descripcion=tarea_created.get("descripcion"),
                fecha_asignacion=tarea_created["fecha_asignacion"],
                fecha_expiracion=tarea_created["fecha_expiracion"],
                estado=tarea_created["estado"]
            )
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error al crear tarea: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear tarea: {str(e)}"
            )


tarea_service = TareaService()
