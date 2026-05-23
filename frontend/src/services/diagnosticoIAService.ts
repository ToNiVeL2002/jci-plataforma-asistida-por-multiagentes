/**
 * Servicio de Diagnóstico con IA (modo batch por área)
 * Maneja la comunicación con el backend para el diagnóstico
 */
import apiClient from './api';

// ============ Interfaces ============

export interface IniciarDiagnosticoRequest {
    id_usuario: string;
    nombre_usuario: string;
    nombre_emprendimiento?: string;
    rubro?: string;
    anio_inicio?: number;
    numero_personal?: number;
    ventas_men_prom?: number;
}

export interface AreaInfo {
    id_area: number;
    nombre_area: string;
}

export interface IniciarDiagnosticoResponse {
    session_id: string;
    user_id: string;
    id_diagnostico: number;
    areas: AreaInfo[];
    mensaje_inicial: string;
}

export interface PreguntaReformulada {
    id_pregunta: number;
    area: string;
    intro: string;
    pregunta: string;
    ejemplo: string;
}

export interface PreguntasAreaRequest {
    session_id: string;
    user_id: string;
    id_area: number;
}

export interface PreguntasTodasRequest {
    session_id: string;
    user_id: string;
}

export interface PreguntasTodasResponse {
    preguntas: PreguntaReformulada[];
}

export interface PreguntasAreaResponse {
    id_area: number;
    nombre_area: string;
    preguntas: PreguntaReformulada[];
}

export interface RespuestaUsuario {
    id_pregunta: number;
    respuesta: string;
}

export interface ScorePregunta {
    id_pregunta: number;
    score: number;
    reason: string;
}

export interface EvaluarAreaRequest {
    session_id: string;
    user_id: string;
    id_area: number;
    respuestas: RespuestaUsuario[];
}

export interface EvaluarAreaResponse {
    scores: ScorePregunta[];
    area_promedio: number;
    inconsistencias: string[];
}

export interface ResultadosRequest {
    session_id: string;
    user_id: string;
    area_scores: { id_area: number; area_promedio: number }[];
}

export interface ResultadosResponse {
    mensaje_despedida: string;
    puntaje_total: number;
}

// Legacy interfaces (mantenidas para compatibilidad)
export interface ChatIARequest {
    session_id: string;
    user_id: string;
    mensaje: string;
}

export interface ChatIAResponse {
    respuesta: string;
}

// ============ Service ============

export const diagnosticoIAService = {
    /**
     * Inicia sesión de diagnóstico (crea sesión ADK + diagnóstico en DB)
     */
    iniciarSesion: async (
        request: IniciarDiagnosticoRequest
    ): Promise<IniciarDiagnosticoResponse> => {
        const response = await apiClient.post<IniciarDiagnosticoResponse>(
            '/diagnostico/ia/iniciar',
            request
        );
        return response.data;
    },

    /**
     * Obtiene preguntas reformuladas de un área
     */
    obtenerPreguntasArea: async (
        request: PreguntasAreaRequest
    ): Promise<PreguntasAreaResponse> => {
        const response = await apiClient.post<PreguntasAreaResponse>(
            '/diagnostico/ia/preguntas-area',
            request
        );
        return response.data;
    },

    /**
     * Obtiene todas las preguntas reformuladas de todas las áreas activas
     */
    obtenerTodasPreguntas: async (
        request: PreguntasTodasRequest
    ): Promise<PreguntasTodasResponse> => {
        const response = await apiClient.post<PreguntasTodasResponse>(
            '/diagnostico/ia/preguntas-todas',
            request
        );
        return response.data;
    },

    /**
     * Evalúa las respuestas de un área
     */
    evaluarArea: async (
        request: EvaluarAreaRequest
    ): Promise<EvaluarAreaResponse> => {
        const response = await apiClient.post<EvaluarAreaResponse>(
            '/diagnostico/ia/evaluar-area',
            request
        );
        return response.data;
    },

    /**
     * Genera resultados finales (conclusión + recomendaciones)
     */
    obtenerResultados: async (
        request: ResultadosRequest
    ): Promise<ResultadosResponse> => {
        const response = await apiClient.post<ResultadosResponse>(
            '/diagnostico/ia/resultados',
            request
        );
        return response.data;
    },

    /**
     * Envía un mensaje al chat legacy
     */
    enviarMensaje: async (
        request: ChatIARequest
    ): Promise<ChatIAResponse> => {
        const response = await apiClient.post<ChatIAResponse>(
            '/diagnostico/ia/chat',
            request
        );
        return response.data;
    },

    /**
     * Finaliza la sesión de diagnóstico
     */
    finalizarSesion: async (sessionId: string, userId: string): Promise<void> => {
        await apiClient.delete(`/diagnostico/ia/finalizar/${sessionId}/${userId}`);
    },

    /**
     * Limpia la sesión si el usuario abandona cerrando pestaña
     */
    limpiarAbandono: (sessionId: string, userId: string): void => {
        // Obtenemos la URL base de apiClient y usamos sendBeacon
        const baseUrl = apiClient.defaults.baseURL || '';
        navigator.sendBeacon(`${baseUrl}/diagnostico/ia/limpiar-abandono/${sessionId}/${userId}`);
    }
};
