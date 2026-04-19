# Frontend - Incubadora JCI

Frontend del sistema de Incubadora de Emprendimientos de la JCI Empresarios La Paz.

## Tecnologías

- **React 18**: Biblioteca para interfaces de usuario
- **TypeScript**: Tipado estático para JavaScript
- **Vite**: Build tool y servidor de desarrollo rápido
- **Tailwind CSS**: Framework de CSS utilitario
- **React Router**: Navegación y routing
- **Supabase**: Autenticación con Google OAuth
- **Axios**: Cliente HTTP para comunicación con backend

## Setup Inicial

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y completa las credenciales:

```bash
copy .env.example .env
```

Edita `.env` con tus credenciales de Supabase y la URL del backend:

```env
VITE_SUPABASE_URL=tu_url_de_supabase
VITE_SUPABASE_ANON_KEY=tu_anon_key_de_supabase
VITE_API_URL=http://localhost:8000
```

### 3. Ejecutar servidor de desarrollo

```bash
npm run dev
```

La aplicación estará disponible en http://localhost:5173

## Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Compila la aplicación para producción
- `npm run preview` - Vista previa de la versión de producción
- `npm run lint` - Ejecuta el linter

## Estructura del Proyecto

```
frontend/
├── public/              # Archivos estáticos
├── src/
│   ├── components/      # Componentes reutilizables
│   │   ├── auth/       # Componentes de autenticación
│   │   └── common/     # Componentes comunes (Button, Card, Sidebar, etc.)
│   ├── context/        # Contextos de React (AuthContext)
│   ├── hooks/          # Hooks personalizados
│   ├── pages/          # Páginas principales
│   │   ├── Login.tsx
│   │   ├── HomeEmprendedor.tsx
│   │   ├── HomeMentor.tsx
│   │   └── HomeAdministrador.tsx
│   ├── services/       # Servicios para API y Supabase
│   ├── types/          # Definiciones de tipos TypeScript
│   ├── App.tsx         # Componente principal con routing
│   ├── main.tsx        # Punto de entrada
│   └── index.css       # Estilos globales y Tailwind
├── .env                # Variables de entorno (NO commitear)
├── .env.example        # Template de variables de entorno
└── package.json
```

## Rutas de la Aplicación

### Rutas Públicas
- `/login` - Página de inicio de sesión con Google

### Rutas Protegidas

**Emprendedor (id_rol = 2):**
- `/emprendedor/home` - Home con opciones de Diagnóstico y Ver Mentor

**Mentor (id_rol = 3):**
- `/mentor/home` - Dashboard con sidebar

**Administrador (id_rol = 1):**
- `/admin/home` - Dashboard con sidebar

## Flujo de Autenticación

1. Usuario accede a `/login`
2. Hace clic en "Continuar con Google"
3. Supabase Auth maneja OAuth con Google
4. Frontend recibe datos del usuario
5. Envía datos al backend para crear/verificar usuario
6. Backend retorna usuario con rol
7. Frontend redirecciona según `id_rol`:
   - `id_rol = 1` → `/admin/home`
   - `id_rol = 2` → `/emprendedor/home`
   - `id_rol = 3` → `/mentor/home`

## Tema y Diseño

El proyecto usa un tema oscuro con colores azul pastel:

- **Primary**: Azul pastel (#0ea5e9 y variantes)
- **Secondary**: Grises azulados
- **Background**: Fondo oscuro (#0f172a)
- **Cards**: Fondo de tarjetas (#1e293b)

Todos los colores y componentes están configurados en:
- `tailwind.config.js` - Configuración de Tailwind
- `src/index.css` - Estilos globales y componentes personalizados

## Notas de Desarrollo

- Las páginas actualmente son **estáticas** (solo estructura)
- Los dashboards y funcionalidades se implementarán en fases posteriores
- La autenticación está completamente funcional
- El routing está protegido por roles
