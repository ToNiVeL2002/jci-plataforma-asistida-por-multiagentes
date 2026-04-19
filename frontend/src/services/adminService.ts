/**
 * Servicio para datos del Administrador
 */
import api from './api';
import type { AdminDashboardData } from '../types/admin';

export interface SeguimientoResult {
    mensaje: string;
    resumen_agente: string;
}

export const adminService = {
    /**
     * Obtiene las estadísticas globales para el dashboard del administrador
     */
    async getAdminDashboard(): Promise<AdminDashboardData> {
        const { data } = await api.get<AdminDashboardData>('/admin/dashboard');
        return data;
    },

    /**
     * Dispara manualmente el agente de seguimiento de tareas.
     * El agente crea una sesión temporal, envía los correos de recordatorio
     * y cierra la sesión automáticamente al terminar.
     */
    async ejecutarSeguimiento(): Promise<SeguimientoResult> {
        const { data } = await api.post<SeguimientoResult>('/seguimiento/ejecutar');
        return data;
    },
};
