/**
 * Modal de Formulario de Datos del Emprendimiento
 * Se muestra cuando el usuario entra a Diagnóstico IA y no tiene emprendimiento registrado
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Rubro } from '../../types/emprendimiento';

export interface EmprendimientoFormData {
    nombre: string;
    rubro: Rubro | '';
    anio_inicio: number | '';
}

interface EmprendimientoFormModalProps {
    onSubmit: (data: EmprendimientoFormData) => Promise<void>;
}

export const EmprendimientoFormModal = ({ onSubmit }: EmprendimientoFormModalProps) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState<EmprendimientoFormData>({
        nombre: '',
        rubro: '',
        anio_inicio: '',
    });
    const [errors, setErrors] = useState<Partial<Record<keyof EmprendimientoFormData, string>>>({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const validate = (): boolean => {
        const newErrors: Partial<Record<keyof EmprendimientoFormData, string>> = {};

        if (!formData.nombre.trim()) {
            newErrors.nombre = 'El nombre del emprendimiento es requerido';
        }
        if (!formData.rubro) {
            newErrors.rubro = 'El rubro es requerido';
        }
        if (!formData.anio_inicio) {
            newErrors.anio_inicio = 'El año de inicio es requerido';
        } else {
            const anio = Number(formData.anio_inicio);
            const currentYear = new Date().getFullYear();
            if (anio < 1900 || anio > currentYear) {
                newErrors.anio_inicio = `El año debe estar entre 1900 y ${currentYear}`;
            }
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!validate()) return;

        setIsSubmitting(true);
        try {
            await onSubmit({
                nombre: formData.nombre,
                rubro: formData.rubro as Rubro,
                anio_inicio: Number(formData.anio_inicio),
            });
        } catch (error) {
            console.error('Error al enviar formulario:', error);
            alert('Error al guardar los datos. Por favor, intenta de nuevo.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        // Clear error when user starts typing
        if (errors[name as keyof EmprendimientoFormData]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const handleCancel = () => {
        navigate(-1); // Go back
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl max-w-md w-full p-5 sm:p-6 border border-light-border">
                {/* Header */}
                <div className="mb-4">
                    <div className="flex items-center justify-center mb-3">
                        <div className="w-12 h-12 bg-primary-500 rounded-full flex items-center justify-center">
                            <svg
                                className="w-6 h-6 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                                />
                            </svg>
                        </div>
                    </div>
                    <h2 className="text-xl sm:text-2xl font-bold text-neutral-900 mb-2 text-center">
                        Cuéntanos sobre tu Emprendimiento
                    </h2>
                    <p className="text-neutral-600 text-xs sm:text-sm text-center">
                        Antes de comenzar el diagnóstico, necesitamos conocer los datos básicos de tu emprendimiento.
                    </p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Nombre del Emprendimiento */}
                    <div>
                        <label htmlFor="nombre" className="block text-sm font-medium text-neutral-700 mb-1.5">
                            Nombre del Emprendimiento <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            lang="es"
                            id="nombre"
                            name="nombre"
                            value={formData.nombre}
                            onChange={handleChange}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 ${errors.nombre ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                            placeholder="Ej: Mi Tiendita"
                        />
                        {errors.nombre && <p className="text-red-500 text-xs mt-1">{errors.nombre}</p>}
                    </div>

                    {/* Rubro */}
                    <div>
                        <label htmlFor="rubro" className="block text-sm font-medium text-neutral-700 mb-1.5">
                            Rubro <span className="text-red-500">*</span>
                        </label>
                        <select
                            id="rubro"
                            name="rubro"
                            value={formData.rubro}
                            onChange={handleChange}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 ${errors.rubro ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                        >
                            <option value="">Selecciona un rubro</option>
                            <option value={Rubro.COMERCIO_VENTAS}>{Rubro.COMERCIO_VENTAS}</option>
                            <option value={Rubro.GASTRONOMIA}>{Rubro.GASTRONOMIA}</option>
                            <option value={Rubro.SERVICIOS_PERSONALES}>{Rubro.SERVICIOS_PERSONALES}</option>
                            <option value={Rubro.ARTES_MANUALIDADES}>{Rubro.ARTES_MANUALIDADES}</option>
                            <option value={Rubro.TECNOLOGIA_EDUCACION}>{Rubro.TECNOLOGIA_EDUCACION}</option>
                            <option value={Rubro.AGRO_PRODUCCION}>{Rubro.AGRO_PRODUCCION}</option>
                            <option value={Rubro.OTROS}>{Rubro.OTROS}</option>
                        </select>
                        {errors.rubro && <p className="text-red-500 text-xs mt-1">{errors.rubro}</p>}
                    </div>

                    {/* Año de Inicio */}
                    <div>
                        <label htmlFor="anio_inicio" className="block text-sm font-medium text-neutral-700 mb-1.5">
                            Año de Inicio <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="number"
                            id="anio_inicio"
                            name="anio_inicio"
                            value={formData.anio_inicio}
                            onChange={handleChange}
                            min="1900"
                            max={new Date().getFullYear()}
                            className={`w-full bg-neutral-50 text-neutral-900 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 ${errors.anio_inicio ? 'ring-2 ring-red-500' : 'focus:ring-blue-500'
                                }`}
                            placeholder="Ej: 2020"
                        />
                        {errors.anio_inicio && <p className="text-red-500 text-xs mt-1">{errors.anio_inicio}</p>}
                    </div>

                    {/* Info Box */}
                    <div className="bg-primary-50 border border-primary-200 rounded-lg p-3">
                        <div className="flex items-start gap-2">
                            <svg
                                className="w-4 h-4 text-primary-500 flex-shrink-0 mt-0.5"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                />
                            </svg>
                            <p className="text-primary-700 text-xs">
                                Esta información básica nos permite configurar tu perfil de emprendedor.
                            </p>
                        </div>
                    </div>

                    {/* Buttons */}
                    <div className="flex gap-3 mt-5">
                        <button
                            type="button"
                            onClick={handleCancel}
                            className="flex-1 bg-neutral-50 hover:bg-neutral-200 text-neutral-900 font-semibold py-2.5 rounded-lg transition-colors"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="flex-1 bg-primary-500 hover:bg-primary-600 text-white font-semibold py-2.5 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isSubmitting ? 'Guardando...' : 'Continuar'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
