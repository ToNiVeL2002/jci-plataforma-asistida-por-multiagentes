/**
 * Servicio de Autenticación
 * Maneja login, logout y autenticación con Google
 */
import { supabase } from './supabaseClient';
import api from './api';
import { User, AuthResponse, GoogleUser } from '../types/user';

export const authService = {
    /**
     * Inicia sesión con Google usando Supabase Auth
     */
    async loginWithGoogle(): Promise<void> {
        const { error } = await supabase.auth.signInWithOAuth({
            provider: 'google',
            options: {
                redirectTo: window.location.origin,
            },
        });

        if (error) {
            throw new Error(`Error al iniciar sesión con Google: ${error.message}`);
        }
    },

    /**
     * Procesa la autenticación después del callback de Google
     * Envía los datos al backend para crear/verificar usuario
     */
    async processGoogleCallback(): Promise<User> {
        try {
            const { data: { session }, error } = await supabase.auth.getSession();

            if (error || !session) {
                throw new Error('No se pudo obtener la sesión de Supabase');
            }

            const user = session.user;

            // Preparar datos para enviar al backend
            const googleUserData: GoogleUser = {
                id: user.id,
                email: user.email!,
                name: user.user_metadata.full_name || user.email!.split('@')[0],
                picture: user.user_metadata.avatar_url,
            };

            // Enviar al backend para crear/verificar usuario con timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

            try {
                const response = await api.post<AuthResponse>('/auth/google', googleUserData, {
                    signal: controller.signal
                });
                clearTimeout(timeoutId);
                return response.data.user;
            } catch (error: any) {
                clearTimeout(timeoutId);
                if (error.name === 'AbortError' || error.code === 'ECONNABORTED') {
                    throw new Error('La solicitud al servidor tomó demasiado tiempo');
                }
                throw new Error(
                    error.response?.data?.detail || 'Error al autenticar con el backend'
                );
            }
        } catch (error: any) {
            console.error('Error en processGoogleCallback:', error);
            throw error;
        }
    },

    /**
     * Obtiene el usuario actual de Supabase
     */
    async getCurrentUser(): Promise<any> {
        const { data: { user } } = await supabase.auth.getUser();
        return user;
    },

    /**
     * Cierra sesión
     * Limpia la sesión de Supabase y el localStorage manualmente
     */
    async logout(): Promise<void> {
        try {
            console.log('[Auth] Iniciando logout...');

            // 1. Limpiar localStorage PRIMERO para que no queden tokens
            const keysToRemove: string[] = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith('sb-')) {
                    keysToRemove.push(key);
                }
            }
            keysToRemove.forEach(key => {
                console.log(`[Auth] Removiendo clave de localStorage: ${key}`);
                localStorage.removeItem(key);
            });

            // 2. Sign out from Supabase
            const { error } = await supabase.auth.signOut({
                scope: 'local'
            });

            if (error) {
                console.error('[Auth] Error en Supabase signOut:', error);
            }

            console.log('[Auth] Logout completado');
        } catch (error: any) {
            console.error('[Auth] Error inesperado en logout:', error);
            // Limpiar localStorage como fallback
            const keys: string[] = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith('sb-')) keys.push(key);
            }
            keys.forEach(k => localStorage.removeItem(k));
        }
    },

    /**
     * Actualiza el perfil del usuario
     */
    async updateUserProfile(userId: string, profileData: {
        nombre: string;
        apellido: string;
        sexo: string;
        fecha_nacimiento: string;
        celular: number;
    }): Promise<User> {
        try {
            const response = await api.put<User>(`/auth/${userId}/profile`, profileData);
            return response.data;
        } catch (error: any) {
            throw new Error(
                error.response?.data?.detail || 'Error al actualizar perfil'
            );
        }
    },
};
