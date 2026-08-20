"""
Servicio de Preguntas
Maneja la lógica de negocio para obtener preguntas del diagnóstico
"""
from typing import Optional, List
from fastapi import HTTPException, status
from app.services.supabase_client import get_supabase_client
from app.models.pregunta import PreguntaResponse, PreguntaConAreaResponse, AreaResponse


class PreguntaService:
    """Servicio para manejar preguntas"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def get_pregunta_by_id(self, id_pregunta: int) -> PreguntaResponse:
        """
        Obtiene una pregunta por su ID
        """
        try:
            response = self.supabase.table("pregunta").select(
                "id_pregunta, id_area, enunciado"
            ).eq("id_pregunta", id_pregunta).execute()
            
            if not response.data or len(response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pregunta con ID {id_pregunta} no encontrada"
                )
            
            pregunta_data = response.data[0]
            
            return PreguntaResponse(
                id_pregunta=pregunta_data["id_pregunta"],
                id_area=pregunta_data["id_area"],
                enunciado=pregunta_data["enunciado"]
            )
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener pregunta: {str(e)}"
            )
    
    async def get_preguntas_by_area(self, id_area: int) -> List[PreguntaConAreaResponse]:
        """
        Obtiene todas las preguntas de un área con el nombre del área que estén activas
        """
        try:
            # Obtener preguntas con join al área y filtradas por estado = True
            response = self.supabase.table("pregunta").select(
                "id_pregunta, id_area, enunciado, area(nombre_area)"
            ).eq("id_area", id_area).eq("estado", True).order("id_pregunta").execute()
            
            if not response.data or len(response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontraron preguntas activas para el área {id_area}"
                )
            
            preguntas = []
            for p in response.data:
                nombre_area = p["area"]["nombre_area"] if isinstance(p.get("area"), dict) else "Desconocida"
                preguntas.append(PreguntaConAreaResponse(
                    id_pregunta=p["id_pregunta"],
                    id_area=p["id_area"],
                    nombre_area=nombre_area,
                    enunciado=p["enunciado"],
                ))
            
            return preguntas
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener preguntas por área: {str(e)}"
            )

    async def get_all_active_preguntas(self) -> List[PreguntaConAreaResponse]:
        """
        Obtiene todas las preguntas activas con el nombre del área, ordenadas por id_area e id_pregunta
        """
        try:
            # Obtener preguntas con join al área ordenadas
            response = self.supabase.table("pregunta").select(
                "id_pregunta, id_area, enunciado, area(nombre_area)"
            ).eq("estado", True).order("id_area").order("id_pregunta").execute()
            
            if not response.data or len(response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontraron preguntas activas"
                )
            
            preguntas = []
            for p in response.data:
                nombre_area = p["area"]["nombre_area"] if isinstance(p.get("area"), dict) else "Desconocida"
                preguntas.append(PreguntaConAreaResponse(
                    id_pregunta=p["id_pregunta"],
                    id_area=p["id_area"],
                    nombre_area=nombre_area,
                    enunciado=p["enunciado"],
                ))
            
            return preguntas
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener todas las preguntas activas: {str(e)}"
            )
    
    async def get_all_areas(self) -> List[AreaResponse]:
        """
        Obtiene todas las áreas ordenadas por id_area
        """
        try:
            response = self.supabase.table("area").select(
                "id_area, nombre_area"
            ).order("id_area").execute()
            
            if not response.data or len(response.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontraron áreas"
                )
            
            return [
                AreaResponse(
                    id_area=a["id_area"],
                    nombre_area=a["nombre_area"],
                )
                for a in response.data
            ]
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener áreas: {str(e)}"
            )
