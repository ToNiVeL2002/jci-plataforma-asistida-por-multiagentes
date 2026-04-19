/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                // JCI Institutional Colors
                jci: {
                    blue: '#00AEEF',
                    dark: '#0F172A',
                    light: '#F8FAFC',
                    gray: '#64748B',
                },
                // Activa Mujer Brand Colors
                activa: {
                    coral: '#F07A5C',
                    amber: '#E8A82E',
                    teal: '#3AADA8',
                    'dark-teal': '#1E766F',
                    peach: '#F5C5A3',
                },
                // JCI Primary Blue mapping for backward compatibility
                primary: {
                    50: '#e0f7ff',
                    100: '#b3eaff',
                    200: '#80dcff',
                    300: '#4dceff',
                    400: '#26c3ff',
                    500: '#00AEEF', // JCI Blue
                    600: '#0099d4',
                    700: '#007eb7',
                    800: '#006597',
                    900: '#00537e',
                    950: '#003554',
                },
                // Activa Teal mapping as secondary
                secondary: {
                    50: '#e2f7f6',
                    100: '#b8eaeb',
                    200: '#89dcdb',
                    300: '#59ccca',
                    400: '#35c0bd',
                    500: '#3AADA8', // Activa Teal
                    600: '#2d8b87',
                    700: '#25706c',
                    800: '#1e5a56',
                    900: '#194947',
                    950: '#0e2b2a',
                },
                // Light mode backgrounds and neutrals
                light: {
                    bg: '#F8FAFC',
                    surface: '#FFFFFF',
                    card: '#FFFFFF',
                    border: '#E2E8F0',
                    hover: '#F1F5F9',
                },
                // Neutral grays for text and UI elements
                neutral: {
                    50: '#f8fafc',
                    100: '#f1f5f9',
                    200: '#e2e8f0',
                    300: '#cbd5e1',
                    400: '#94a3b8',
                    500: '#64748b',
                    600: '#475569',
                    700: '#334155',
                    800: '#1e293b',
                    900: '#0f172a',
                }
            },
        },
    },
    plugins: [],
}
