# Backend - Incubadora JCI

Backend del sistema de Incubadora de Emprendimientos de la JCI Empresarios La Paz.

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Supabase**: Base de datos PostgreSQL y autenticación
- **Python 3.9+**: Lenguaje de programación

## Setup Inicial

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y completa las credenciales:

```bash
copy .env.example .env
```

Edita `.env` con tus credenciales de Supabase.

### 5. Ejecutar servidor de desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- API: http://localhost:8000
- Documentación interactiva (Swagger): http://localhost:8000/docs
- Documentación alternativa (ReDoc): http://localhost:8000/redoc

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── config.py            # Configuración y variables de entorno
│   ├── models/              # Modelos Pydantic
│   ├── services/            # Lógica de negocio
│   └── routers/             # Endpoints de la API
├── .env                     # Variables de entorno (NO commitear)
├── .env.example             # Template de variables de entorno
├── requirements.txt         # Dependencias Python
└── README.md
```

## Endpoints Disponibles

### Autenticación

- `POST /auth/google` - Autenticación con Google OAuth
- `GET /auth/me` - Obtener datos del usuario actual

## Variables de Entorno Requeridas

- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_KEY`: Service Key de Supabase
- `ALLOWED_ORIGINS`: URLs permitidas para CORS (frontend)
