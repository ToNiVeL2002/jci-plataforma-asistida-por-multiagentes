"""
Servicio de Administrador
Maneja la lógica de negocio para estadísticas globales del administrador
"""
from typing import Optional
from fastapi import HTTPException, status
from app.services.supabase_client import get_supabase_client
from app.models.admin import AdminDashboardResponse


class AdminService:
    """Servicio para manejar estadísticas del administrador"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def get_dashboard_stats(self) -> AdminDashboardResponse:
        """
        Obtiene estadísticas globales para el dashboard del administrador
        
        Returns:
            AdminDashboardResponse: Estadísticas globales
        
        Raises:
            HTTPException: Si hay error al obtener las estadísticas
        """
        try:
            # 1. Total de emprendedores (rol = 2, estado = true)
            emprendedores_response = self.supabase.table("usuario") \
                .select("id_usuario", count="exact") \
                .eq("id_rol", 2) \
                .eq("estado", True) \
                .execute()
            
            total_emprendedores = emprendedores_response.count or 0
            
            # 2. Total de mentores activos (rol = 3, estado = true)
            mentores_response = self.supabase.table("usuario") \
                .select("id_usuario", count="exact") \
                .eq("id_rol", 3) \
                .eq("estado", True) \
                .execute()
            
            total_mentores_activos = mentores_response.count or 0
            
            # 3. Diagnósticos completados (con resultado no vacío)
            diagnosticos_response = self.supabase.table("diagnostico") \
                .select("id_usuario, fecha_inicio, id_diagnostico, resultado, puntaje_total, puntaje_cf, puntaje_gp, puntaje_m, puntaje_v, puntaje_tp, puntaje_rh") \
                .not_.is_("resultado", "null") \
                .neq("resultado", "") \
                .execute()
            
            diagnosticos_data = diagnosticos_response.data
            
            # Agrupar por id_usuario y mantener solo el más reciente
            ultimos_diagnosticos_map = {}
            for diag in diagnosticos_data:
                user_id = diag.get("id_usuario")
                if not user_id: 
                    continue
                if user_id not in ultimos_diagnosticos_map:
                    ultimos_diagnosticos_map[user_id] = diag
                else:
                    fecha_actual = diag.get("fecha_inicio")
                    fecha_guardada = ultimos_diagnosticos_map[user_id].get("fecha_inicio")
                    if fecha_actual and fecha_guardada and str(fecha_actual) > str(fecha_guardada):
                        ultimos_diagnosticos_map[user_id] = diag
                        
            diagnosticos = list(ultimos_diagnosticos_map.values())
            diagnosticos_completados = len(diagnosticos)
            
            # 4. Calcular tasa de éxito
            if diagnosticos_completados > 0:
                aceptados = sum(1 for d in diagnosticos if d.get("resultado") == "ACEPTADO")
                tasa_exito = round((aceptados / diagnosticos_completados) * 100, 2)
            else:
                tasa_exito = 0.0
            
            # 5. Calcular promedios por área
            if diagnosticos_completados > 0:
                sum_total = sum(d.get("puntaje_total", 0) or 0 for d in diagnosticos)
                sum_cf = sum(d.get("puntaje_cf", 0) or 0 for d in diagnosticos)
                sum_gp = sum(d.get("puntaje_gp", 0) or 0 for d in diagnosticos)
                sum_m = sum(d.get("puntaje_m", 0) or 0 for d in diagnosticos)
                sum_v = sum(d.get("puntaje_v", 0) or 0 for d in diagnosticos)
                sum_tp = sum(d.get("puntaje_tp", 0) or 0 for d in diagnosticos)
                sum_rh = sum(d.get("puntaje_rh", 0) or 0 for d in diagnosticos)
                
                promedio_general = round(sum_total / diagnosticos_completados, 2)
                promedio_cf = round(sum_cf / diagnosticos_completados, 2)
                promedio_gp = round(sum_gp / diagnosticos_completados, 2)
                promedio_m = round(sum_m / diagnosticos_completados, 2)
                promedio_v = round(sum_v / diagnosticos_completados, 2)
                promedio_tp = round(sum_tp / diagnosticos_completados, 2)
                promedio_rh = round(sum_rh / diagnosticos_completados, 2)
            else:
                promedio_general = 0.0
                promedio_cf = 0.0
                promedio_gp = 0.0
                promedio_m = 0.0
                promedio_v = 0.0
                promedio_tp = 0.0
                promedio_rh = 0.0
            
            return AdminDashboardResponse(
                total_emprendedores=total_emprendedores,
                total_mentores_activos=total_mentores_activos,
                diagnosticos_completados=diagnosticos_completados,
                tasa_exito=tasa_exito,
                promedio_general=promedio_general,
                promedio_cf=promedio_cf,
                promedio_gp=promedio_gp,
                promedio_m=promedio_m,
                promedio_v=promedio_v,
                promedio_tp=promedio_tp,
                promedio_rh=promedio_rh
            )
            
        except Exception as e:
            print(f"Error al obtener estadísticas del administrador: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener estadísticas: {str(e)}"
            )


admin_service = AdminService()
