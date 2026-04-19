/**
 * Menú de navegación compartido para todas las páginas del Administrador.
 * Actualizar AQUÍ para que el cambio se refleje en toda la sección admin.
 */
import type { MenuItem } from '../components/common/Sidebar';

export const ADMIN_MENU_ITEMS: MenuItem[] = [
    { label: 'Dashboard',             path: '/admin/home' },
    { label: 'Gestión de Usuarios',   path: '/admin/usuarios' },
    { label: 'Asignar Mentores',      path: '/admin/asignar-mentores' },
    { label: 'Generar Reportes',      path: '/admin/reportes' },
    { label: 'Seguimiento de Tareas', path: '/admin/seguimiento' },
];
