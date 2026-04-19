/**
 * Página de Cuenta Deshabilitada
 * Se muestra cuando un usuario con estado=False intenta acceder al sistema
 */
import { useNavigate } from 'react-router-dom';

export const AccountDisabled = () => {
    const navigate = useNavigate();

    const handleGoToLogin = () => {
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-light-bg flex items-center justify-center p-4">
            <div className="max-w-md w-full text-center">
                {/* Icon */}
                <div className="mb-6">
                    <svg
                        className="w-24 h-24 mx-auto text-red-500"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                        />
                    </svg>
                </div>

                {/* Title */}
                <h1 className="text-3xl font-bold text-neutral-900 mb-4">
                    Cuenta Deshabilitada
                </h1>

                {/* Message */}
                <p className="text-neutral-600 text-lg mb-8">
                    Su cuenta ha sido deshabilitada del sistema. Por favor, contacte al administrador para más información.
                </p>

                {/* Button */}
                <button
                    onClick={handleGoToLogin}
                    className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors duration-200"
                >
                    Volver al Inicio de Sesión
                </button>

                {/* Contact Info */}
                <div className="mt-8 pt-8 border-t border-light-border">
                    <p className="text-gray-500 text-sm">
                        ¿Necesitas ayuda? Contacta al administrador del sistema.
                    </p>
                </div>
            </div>
        </div>
    );
};
