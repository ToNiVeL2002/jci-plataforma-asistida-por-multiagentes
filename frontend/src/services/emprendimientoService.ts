/**
 * Servicio de Emprendimiento
 * Maneja operaciones relacionadas con emprendimientos y sus estados
 */
import api from './api';
import { Emprendimiento, EstadoEmprendimiento } from '../types/emprendimiento';

/**
 * Request para crear emprendimiento
 */
interface CreateEmprendimientoRequest {
    id_usuario: string;
    nombre: string;
    rubro: string;
    anio_inicio: number;
}

/**
 * Request para crear estado de emprendimiento
 */
interface CreateEstadoEmprendimientoRequest {
    id_emprendimiento: number;
    numero_personal: number;
    ventas_men_prom: number;
}

export const emprendimientoService = {
    /**
     * Crea un nuevo emprendimiento para un usuario
     */
    async createEmprendimiento(data: CreateEmprendimientoRequest): Promise<Emprendimiento> {
        try {
            const response = await api.post<Emprendimiento>('/emprendimiento', data);
            return response.data;
        } catch (error: any) {
            throw new Error(
                error.response?.data?.detail || 'Error al crear emprendimiento'
            );
        }
    },

    /**
     * Obtiene el emprendimiento de un usuario
     */
    async getEmprendimientoByUser(idUsuario: string): Promise<Emprendimiento | null> {
        try {
            const response = await api.get<Emprendimiento | null>(
                `/emprendimiento/usuario/${idUsuario}`
            );
            return response.data;
        } catch (error: any) {
            throw new Error(
                error.response?.data?.detail || 'Error al obtener emprendimiento'
            );
        }
    },

    /**
     * Crea un nuevo registro de estado del emprendimiento
     */
    async createEstadoEmprendimiento(
        data: CreateEstadoEmprendimientoRequest
    ): Promise<EstadoEmprendimiento> {
        try {
            const response = await api.post<EstadoEmprendimiento>(
                '/emprendimiento/estado',
                data
            );
            return response.data;
        } catch (error: any) {
            throw new Error(
                error.response?.data?.detail || 'Error al crear estado del emprendimiento'
            );
        }
    },

    /**
     * Obtiene el historial de estados de un emprendimiento
     */
    async getEstadosEmprendimiento(idEmprendimiento: number): Promise<EstadoEmprendimiento[]> {
        try {
            const response = await api.get<EstadoEmprendimiento[]>(
                `/emprendimiento/${idEmprendimiento}/estados`
            );
            return response.data;
        } catch (error: any) {
            throw new Error(
                error.response?.data?.detail || 'Error al obtener estados del emprendimiento'
            );
        }
    },
};
