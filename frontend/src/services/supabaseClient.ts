/**
 * Cliente de Supabase
 */
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error('Faltan variables de entorno de Supabase. Por favor configura VITE_SUPABASE_URL y VITE_SUPABASE_ANON_KEY');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        persistSession: true,
        detectSessionInUrl: true,
        flowType: 'pkce', // Más seguro que implicit
        autoRefreshToken: true,
        storageKey: 'jci-auth', // Clave personalizada para evitar conflictos
    }
});
