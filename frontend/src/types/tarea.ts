/**
 * Tipos TypeScript para el módulo de Tareas
 */

export interface TareaCreate {
    id_usuario: string;
    id_diagnostico: number;
    titulo: string;
    descripcion?: string;
    fecha_expiracion: string; // ISO string
}

export interface Tarea {
    id_tarea: number;
    id_usuario: string;
    id_diagnostico: number;
    titulo: string;
    descripcion: string | null;
    fecha_asignacion: string;
    fecha_expiracion: string;
    estado: string;
}
