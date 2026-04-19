/**
 * Componente Button reutilizable
 */
import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary';
    children: React.ReactNode;
}

export const Button = ({ variant = 'primary', children, className = '', ...props }: ButtonProps) => {
    const baseClasses = 'font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105';
    const variantClasses = {
        primary: 'bg-primary-600 hover:bg-primary-700 text-white shadow-lg',
        secondary: 'bg-secondary-600 hover:bg-secondary-700 text-neutral-900 shadow-lg',
    };

    return (
        <button
            className={`${baseClasses} ${variantClasses[variant]} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
};
