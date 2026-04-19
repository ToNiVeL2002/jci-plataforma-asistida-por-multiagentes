/**
 * Contexto de Autenticación
 * Proporciona estado global de autenticación
 */
import { createContext, useContext, useState, useEffect, useCallback, useRef, ReactNode } from 'react';
import { User } from '../types/user';
import { authService } from '../services/authService';
import { supabase } from '../services/supabaseClient';

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: () => Promise<void>;
    logout: () => Promise<void>;
    setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    // Use refs instead of state to avoid stale closures in useEffect
    const isProcessingRef = useRef(false);
    const isLoggingOutRef = useRef(false);

    useEffect(() => {
        // Verificar sesión al cargar la app
        checkSession();

        // Suscribirse a cambios de autenticación
        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            async (event, session) => {
                // Evitar procesar múltiples veces o durante logout
                if (isProcessingRef.current || isLoggingOutRef.current) return;

                if (event === 'SIGNED_IN' && session) {
                    isProcessingRef.current = true;
                    try {
                        const userData = await authService.processGoogleCallback();

                        // Verificar si el usuario está deshabilitado
                        if (!userData.estado) {
                            // Usuario deshabilitado - cerrar sesión y redirigir
                            await authService.logout();
                            setUser(null);
                            window.location.href = '/account-disabled';
                            return;
                        }

                        setUser(userData);
                    } catch (error) {
                        console.error('Error al procesar callback:', error);
                    } finally {
                        isProcessingRef.current = false;
                    }
                } else if (event === 'SIGNED_OUT') {
                    isProcessingRef.current = false;
                    isLoggingOutRef.current = false;
                    setUser(null);
                }
            }
        );

        return () => {
            subscription.unsubscribe();
        };
    }, []); // Can safely keep empty array now since we use refs

    const checkSession = async () => {
        if (isProcessingRef.current || isLoggingOutRef.current) return;

        isProcessingRef.current = true;
        try {
            const { data: { session } } = await supabase.auth.getSession();

            if (session?.user) {
                try {
                    const userData = await authService.processGoogleCallback();

                    // Verificar si el usuario está deshabilitado
                    if (!userData.estado) {
                        // Usuario deshabilitado - cerrar sesión y redirigir
                        await authService.logout();
                        setUser(null);
                        window.location.href = '/account-disabled';
                        return;
                    }

                    setUser(userData);
                } catch (error: any) {
                    console.error('Error al verificar sesión:', error);
                    if (error.response?.status === 403) {
                        // Usuario deshabilitado
                        await authService.logout();
                        window.location.href = '/account-disabled';
                    } else {
                        // Otro error - limpiar sesión
                        await authService.logout();
                        setUser(null);
                    }
                }
            } else {
                setUser(null);
            }
        } catch (error) {
            console.error('Error en checkSession:', error);
            setUser(null);
        } finally {
            setLoading(false);
            isProcessingRef.current = false;
        }
    };

    const login = useCallback(async () => {
        await authService.loginWithGoogle();
    }, []);

    const logout = useCallback(async () => {
        console.log('[AuthContext] Logout solicitado');
        isLoggingOutRef.current = true;
        isProcessingRef.current = false;

        // Limpiar usuario del estado inmediatamente
        setUser(null);

        try {
            await authService.logout();
            console.log('[AuthContext] Logout completado, redirigiendo...');
        } catch (error) {
            console.error('[AuthContext] Error al cerrar sesión:', error);
        } finally {
            // Siempre redirigir, incluso si Supabase falla
            window.location.replace('/login');
        }
    }, []);

    return (
        <AuthContext.Provider value={{ user, loading, login, logout, setUser }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth debe ser usado dentro de AuthProvider');
    }
    return context;
};
