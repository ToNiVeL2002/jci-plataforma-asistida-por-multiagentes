/**
 * Componente de rutas protegidas
 */
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

interface ProtectedRouteProps {
    children: React.ReactNode;
    allowedRoles: number[];
}

export const ProtectedRoute = ({ children, allowedRoles }: ProtectedRouteProps) => {
    const { user, loading } = useAuth();

    if (loading) {
        return (
            <div className="min-h-screen bg-light-bg flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500 mx-auto"></div>
                    <p className="text-neutral-600 mt-4">Cargando...</p>
                </div>
            </div>
        );
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (!allowedRoles.includes(user.id_rol)) {
        // Redireccionar al home correcto según su rol
        if (user.id_rol === 1) return <Navigate to="/admin/home" replace />;
        if (user.id_rol === 2) return <Navigate to="/emprendedor/home" replace />;
        if (user.id_rol === 3) return <Navigate to="/mentor/home" replace />;
    }

    return <>{children}</>;
};
