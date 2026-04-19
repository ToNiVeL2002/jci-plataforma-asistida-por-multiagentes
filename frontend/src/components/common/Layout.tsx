/**
 * Componente Layout para páginas con sidebar
 * Maneja el estado del sidebar en móvil (hamburger menu)
 */
import { ReactNode, useState, useCallback } from 'react';
import { Sidebar, MenuItem } from './Sidebar';

interface LayoutProps {
    children: ReactNode;
    menuItems?: MenuItem[];
    onLogout?: () => void;
}

export const Layout = ({ children, menuItems, onLogout }: LayoutProps) => {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    const handleOpen = useCallback(() => setSidebarOpen(true), []);
    const handleClose = useCallback(() => setSidebarOpen(false), []);

    const hasSidebar = menuItems && onLogout;

    return (
        // 1. CAMBIO AQUÍ: h-screen en lugar de min-h-screen, y añadimos overflow-hidden
        <div className="flex h-screen bg-light-surface text-neutral-900 overflow-hidden">
            {/* Sidebar */}
            {hasSidebar && (
                <Sidebar
                    menuItems={menuItems}
                    onLogout={onLogout}
                    isOpen={sidebarOpen}
                    onClose={handleClose}
                />
            )}

            {/* Main Content */}
            {/* 2. CAMBIO AQUÍ: añadimos overflow-hidden a la columna para que respete el h-screen */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
                {/* Mobile Header with hamburger (only when sidebar exists) */}
                {hasSidebar && (
                    <header 
                        className="lg:hidden sticky top-0 z-30 px-4 py-3 flex items-center gap-3 shadow-md border-b border-white/10"
                        style={{
                            background: 'linear-gradient(160deg, #0b1a30 0%, #112B56 30%, #0f5c7a 70%, #0a7060 100%)'
                        }}
                    >
                        <button
                            onClick={handleOpen}
                            className="text-white p-1 rounded-lg hover:bg-primary-400 transition-colors"
                            aria-label="Abrir menú"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                        <h1 className="text-white font-semibold text-lg">Incubadora JCI</h1>
                    </header>
                )}

                {/* Page Content */}
                {/* 3. CAMBIO AQUÍ: añadimos overflow-y-auto para que genere la barra de desplazamiento */}
                <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-x-hidden overflow-y-auto">
                    {children}
                </main>
            </div>
        </div>
    );
};