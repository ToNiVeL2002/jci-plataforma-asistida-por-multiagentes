/**
 * Componente Card reutilizable
 */
import { ReactNode } from 'react';

interface CardProps {
    children: ReactNode;
    className?: string;
    onClick?: () => void;
    hoverable?: boolean;
}

export const Card = ({ children, className = '', onClick, hoverable = false }: CardProps) => {
    const hoverClasses = hoverable ? 'cursor-pointer hover:shadow-2xl hover:scale-105 hover:border-primary-500' : '';

    return (
        <div
            className={`card transition-all duration-300 ${hoverClasses} ${className}`}
            onClick={onClick}
        >
            {children}
        </div>
    );
};
