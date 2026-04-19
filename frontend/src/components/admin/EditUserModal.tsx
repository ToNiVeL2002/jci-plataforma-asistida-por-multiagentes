/**
 * Modal para editar rol y permisos de un usuario
 */
import { useState } from 'react';
import { User } from '../../types/user';

interface EditUserModalProps {
    user: User;
    onSubmit: (idRol: number, habilitadoDiag: boolean, estado: boolean) => Promise<void>;
    onClose: () => void;
}

const ROLES = [
    { id: 1, name: 'Administrador' },
    { id: 2, name: 'Emprendedor' },
    { id: 3, name: 'Mentor' },
];

export const EditUserModal = ({ user, onSubmit, onClose }: EditUserModalProps) => {
    const [idRol, setIdRol] = useState(user.id_rol);
    const [habilitadoDiag, setHabilitadoDiag] = useState(user.habilitado_diag);
    const [estado, setEstado] = useState(user.estado);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        setIsSubmitting(true);
        try {
            await onSubmit(idRol, habilitadoDiag, estado);
        } catch (error) {
            console.error('Error al actualizar usuario:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl max-w-md w-full p-6 border border-light-border">
                {/* Header */}
                <div className="mb-6">
                    <h2 className="text-2xl font-bold text-neutral-900 mb-1">
                        Editar Usuario
                    </h2>
                    <p className="text-neutral-600 text-sm">
                        {user.nombre && user.apellido
                            ? `${user.nombre} ${user.apellido}`
                            : user.nombre || user.apellido || user.email}
                    </p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Rol Selection */}
                    <div>
                        <label htmlFor="rol" className="block text-sm font-medium text-neutral-700 mb-2">
                            Rol
                        </label>
                        <select
                            id="rol"
                            value={idRol}
                            onChange={(e) => setIdRol(parseInt(e.target.value))}
                            className="w-full bg-neutral-50 text-neutral-900 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            {ROLES.map((role) => (
                                <option key={role.id} value={role.id}>
                                    {role.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Estado Toggle */}
                    <div className="pt-2">
                        <label className="flex items-center justify-between cursor-pointer">
                            <span className="text-sm font-medium text-neutral-700">
                                Usuario habilitado
                            </span>
                            <div className="relative">
                                <input
                                    type="checkbox"
                                    checked={estado}
                                    onChange={(e) => setEstado(e.target.checked)}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-neutral-200 peer-focus:ring-2 peer-focus:ring-green-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                            </div>
                        </label>
                        <p className="text-xs text-gray-500 mt-1">
                            {estado ? 'El usuario puede acceder al sistema' : 'El usuario está deshabilitado y no puede iniciar sesión'}
                        </p>
                    </div>

                    {/* Habilitado Diag Toggle */}
                    <div className="pt-2">
                        <label className="flex items-center justify-between cursor-pointer">
                            <span className="text-sm font-medium text-neutral-700">
                                Diagnóstico con IA habilitado
                            </span>
                            <div className="relative">
                                <input
                                    type="checkbox"
                                    checked={habilitadoDiag}
                                    onChange={(e) => setHabilitadoDiag(e.target.checked)}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-neutral-200 peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                            </div>
                        </label>
                        <p className="text-xs text-gray-500 mt-1">
                            {habilitadoDiag ? 'El usuario puede acceder al chat con IA' : 'El acceso al diagnóstico está deshabilitado'}
                        </p>
                    </div>

                    {/* Buttons */}
                    <div className="flex gap-3 mt-6">
                        <button
                            type="button"
                            onClick={onClose}
                            disabled={isSubmitting}
                            className="flex-1 bg-neutral-50 hover:bg-neutral-200 text-neutral-900 font-semibold py-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="flex-1 bg-primary-500 hover:bg-primary-600 text-white font-semibold py-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isSubmitting ? 'Guardando...' : 'Guardar'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
