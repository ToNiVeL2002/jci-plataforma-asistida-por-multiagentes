# Incubadora JCI - Empresarios La Paz

Sistema de gestión para la Incubadora de Emprendimientos de la JCI Empresarios La Paz.

## Estructura del Proyecto

```
jci-proyecto/
├── backend/          # Backend con FastAPI
└── frontend/         # Frontend con React
```

## Tecnologías

### Backend
- FastAPI
- Supabase (PostgreSQL + Auth)
- Python 3.9+

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Vite

## Setup Completo

### 1. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales de Supabase

# Ejecutar servidor
uvicorn app.main:app --reload
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

### 2. Frontend

> **Nota**: Si tienes problemas con la ejecución de scripts en PowerShell, ejecuta:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales de Supabase

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 🔐 Configuración de Credenciales y Entorno

> **Aviso de Seguridad:** Todos los archivos `.env` donde se guarda la información sensible están excluidos del control de versiones mediante el archivo `.gitignore`. **Es completamente seguro hacer este repositorio público** para tu currículum; ninguna de tus claves reales (de Supabase o Gemini) será subida a GitHub.

Las llaves, contraseñas y accesos se manejan exclusivamente a través de los siguientes archivos locales `.env`. Quien clone este proyecto deberá crearlos manualmente basándose en los `.env.example` proporcionados de la siguiente manera:

### 1. Variables de Supabase y Backend

**Ubicación: `backend/.env`**
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_service_role_key_supabase
API_HOST=0.0.0.0
API_PORT=8000
```

**Ubicación: `frontend/.env`**
```env
VITE_SUPABASE_URL=https://tu-proyecto.supabase.co
VITE_SUPABASE_ANON_KEY=tu_anon_key_supabase
VITE_API_URL=http://localhost:8000
```

### 2. Variables de Agentes IA (Google Gemini y Gmail)

**Ubicación: `IA/multi_agente_diagnostico/.env`**
Maneja el diagnóstico de la incubadora con Gemini.
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY="tu_google_gemini_api_key"
```

**Ubicación: `IA/multi_agente_seguimiento/.env`**
Envía correos con recordatorios a los estudiantes emprendedores (USA cuenta de envío SMTP).
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY="tu_google_gemini_api_key"
EMAIL_SENDER="tu_correo_gmail@gmail.com"
EMAIL_PASSWORD="app_password_de_tu_gmail"
```

### Configurar Google OAuth en Supabase

1. Ve a tu proyecto en Supabase
2. Navega a Authentication → Providers
3. Habilita Google Provider
4. Configura las credenciales de Google OAuth

## Usuarios y Roles

El sistema tiene 3 tipos de usuarios:

1. **Administrador** (id_rol = 1)
   - Dashboard
   - Gestión de usuarios
   - Generar reportes

2. **Emprendedor** (id_rol = 2) - Rol por defecto
   - Diagnóstico con IA
   - Ver mentor asignado

3. **Mentor** (id_rol = 3)
   - Dashboard
   - Resultados de diagnóstico
   - Asignar tareas
   - Generar reportes

## Flujo de Login

1. Usuario hace clic en "Continuar con Google"
2. Supabase maneja autenticación OAuth
3. Backend crea usuario si no existe (con rol Emprendedor)
4. Frontend redirecciona según rol:
   - Admin → `/admin/home`
   - Emprendedor → `/emprendedor/home`
   - Mentor → `/mentor/home`

## Estado Actual

✅ **Fase 1 Completada:**
- Sistema de autenticación con Google OAuth
- Login funcional
- 3 pantallas estáticas (una por cada rol)
- Routing protegido por roles
- Backend con endpoints REST
- Integración completa Frontend-Backend

⏳ **Próximas Fases:**
- Funcionalidad de módulos (Diagnóstico, Tareas, Reportes, etc.)
- Dashboards con datos reales
- Gestión de usuarios por administrador
- Y más...

## Arquitectura

- **Backend**: Toda la lógica de negocio está en el backend
- **Frontend**: Solo UI y comunicación con API
- **Base de Datos**: Supabase (PostgreSQL)
- **Autenticación**: Supabase Auth con Google OAuth

## Desarrollo

Para más detalles sobre cada parte del proyecto, consulta:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## Notas de PowerShell

Si encuentras el error "la ejecución de scripts está deshabilitada", ejecuta este comando en PowerShell como Administrador:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
