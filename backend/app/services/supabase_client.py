"""
Cliente de Supabase
Proporciona una instancia singleton del cliente de Supabase
"""
from supabase import create_client, Client
from app.config import settings

_supabase_client: Client = None

def get_supabase_client() -> Client:
    global _supabase_client
    
    if _supabase_client is None:
        _supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
    return _supabase_client
