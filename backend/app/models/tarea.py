"""
Modelos Pydantic para el módulo de Tareas
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
from typing import Optional


class TareaCreate(BaseModel):
    """
    Modelo para crear una nueva tarea
    """
    id_usuario: str  # UUID del emprendedor
    id_diagnostico: int
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    fecha_expiracion: datetime
    
    @validator('fecha_expiracion')
    def validate_expiration(cls, v):
        """Validar que la fecha de expiración sea al menos 1 día en el futuro"""
        # Asegurar que ambas fechas sean timezone-aware para comparación
        from datetime import timezone
        
        # Si v tiene timezone, usar now con timezone
        if v.tzinfo is not None:
            now = datetime.now(timezone.utc)
        else:
            now = datetime.now()
        
        min_date = now + timedelta(days=1)
        
        if v <= min_date:
            raise ValueError('La fecha de expiración debe ser al menos 1 día en el futuro')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id_usuario": "550e8400-e29b-41d4-a716-446655440000",
                "id_diagnostico": 1,
                "titulo": "Mejorar plan de marketing",
                "descripcion": "Revisar y actualizar el plan de marketing según los resultados del diagnóstico",
                "fecha_expiracion": "2024-12-31T23:59:59"
            }
        }


class TareaResponse(BaseModel):
    """
    Modelo de respuesta de una tarea
    """
    id_tarea: int
    id_usuario: str
    id_diagnostico: int
    titulo: str
    descripcion: Optional[str]
    fecha_asignacion: datetime
    fecha_expiracion: datetime
    estado: str
    
    class Config:
        from_attributes = True
