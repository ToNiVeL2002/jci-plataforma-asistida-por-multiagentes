/**
 * Modal de Formulario de Datos Personales
 * Se muestra cuando el usuario no tiene nombre registrado
 */
import { useState } from 'react';

interface ProfileFormModalProps {
    onSubmit: (data: ProfileFormData) => Promise<void>;
}

export interface ProfileFormData {
    nombre: string;
    apellido: string;
    sexo: string;
    fecha_nacimiento: string;
    celular: string;
}

export const ProfileFormModal = ({ onSubmit }: ProfileFormModalProps) => {
    const [formData, setFormData] = useState<ProfileFormData>({
        nombre: '',
        apellido: '',
        sexo: '',
        fecha_nacimiento: '',
        celular: '',
    });
    const [errors, setErrors] = useState<Partial<Record<keyof ProfileFormData, string>>>({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const validate = (): boolean => {
        const newErrors: Partial<Record<keyof ProfileFormData, string>> = {};

        // Validaciones de datos personales
        if (!formData.nombre.trim()) newErrors.nombre = 'El nombre es requerido';
        if (!formData.apellido.trim()) newErrors.apellido = 'El apellido es requerido';
        if (!formData.sexo) newErrors.sexo = 'El sexo es requerido';
        if (!formData.fecha_nacimiento) newErrors.fecha_nacimiento = 'La fecha de nacimiento es requerida';
        if (!formData.celular.trim()) {
            newErrors.celular = 'El celular es requerido';
        } else if (!/^\d{8,15}$/.test(formData.celular)) {
            newErrors.celular = 'El celular debe tener entre 8 y 15 dígitos';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!validate()) return;

        setIsSubmitting(true);
        try {
            await onSubmit(formData);
        } catch (error) {
            console.error('Error al enviar formulario:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        // Clear error when user starts typing
        if (errors[name as keyof ProfileFormData]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl max-w-md w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 border border-light-border">
                {/* Header */}
                <div className="mb-6">
                    <h2 className="text-2xl sm:text-3xl font-bold text-neutral-900 mb-2">
                        Completa tu Perfil
                    </h2>
                    <p className="text-neutral-600 text-sm">
                        Para continuar, necesitamos algunos datos personales.
                    </p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Nombre */}
                    <div>
                        <label htmlFor="nombre" className="block text-sm font-medium text-neutral-700 mb-1">
                            Nombre <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            lang="es"
                            id="nombre"
                            name="nombre"
                            value={formData.nombre}
                            onChange={handleChange}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 ${errors.nombre ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                            placeholder="Ingresa tu nombre"
                        />
                        {errors.nombre && <p className="text-red-500 text-xs mt-1">{errors.nombre}</p>}
                    </div>

                    {/* Apellido */}
                    <div>
                        <label htmlFor="apellido" className="block text-sm font-medium text-neutral-700 mb-1">
                            Apellido <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            lang="es"
                            id="apellido"
                            name="apellido"
                            value={formData.apellido}
                            onChange={handleChange}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 ${errors.apellido ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                            placeholder="Ingresa tu apellido"
                        />
                        {errors.apellido && <p className="text-red-500 text-xs mt-1">{errors.apellido}</p>}
                    </div>

                    {/* Sexo */}
                    <div>
                        <label htmlFor="sexo" className="block text-sm font-medium text-neutral-700 mb-1">
                            Sexo <span className="text-red-500">*</span>
                        </label>
                        <select
                            id="sexo"
                            name="sexo"
                            value={formData.sexo}
                            onChange={handleChange}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 ${errors.sexo ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                        >
                            <option value="">Selecciona una opción</option>
                            <option value="M">Masculino</option>
                            <option value="F">Femenino</option>
                            <option value="O">Otro</option>
                        </select>
                        {errors.sexo && <p className="text-red-500 text-xs mt-1">{errors.sexo}</p>}
                    </div>

                    {/* Fecha de Nacimiento */}
                    <div>
                        <label htmlFor="fecha_nacimiento" className="block text-sm font-medium text-neutral-700 mb-1">
                            Fecha de Nacimiento <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="date"
                            id="fecha_nacimiento"
                            name="fecha_nacimiento"
                            value={formData.fecha_nacimiento}
                            onChange={handleChange}
                            max={new Date().toISOString().split('T')[0]}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 ${errors.fecha_nacimiento ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                        />
                        {errors.fecha_nacimiento && <p className="text-red-500 text-xs mt-1">{errors.fecha_nacimiento}</p>}
                    </div>

                    {/* Celular */}
                    <div>
                        <label htmlFor="celular" className="block text-sm font-medium text-neutral-700 mb-1">
                            Celular <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="tel"
                            id="celular"
                            name="celular"
                            value={formData.celular}
                            onChange={handleChange}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 ${errors.celular ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                            placeholder="Ej: 79123456"
                        />
                        {errors.celular && <p className="text-red-500 text-xs mt-1">{errors.celular}</p>}
                    </div>


                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="w-full bg-primary-500 hover:bg-primary-600 text-white font-semibold py-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-6"
                    >
                        {isSubmitting ? 'Guardando...' : 'Guardar Datos'}
                    </button>
                </form>
            </div>
        </div>
    );
};
