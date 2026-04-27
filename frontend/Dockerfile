# ============================================================
# Stage 1: builder — compila el proyecto TypeScript/React
# ============================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar dependencias primero (mejor cache)
COPY package.json package-lock.json ./
RUN npm ci

# Copiar código fuente y construir
# Las variables VITE_* se inyectan como build args
ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_ANON_KEY
ARG VITE_API_URL=http://localhost:8000

ENV VITE_SUPABASE_URL=$VITE_SUPABASE_URL
ENV VITE_SUPABASE_ANON_KEY=$VITE_SUPABASE_ANON_KEY
ENV VITE_API_URL=$VITE_API_URL

COPY . .
RUN npm run build

# ============================================================
# Stage 2: runner — sirve el build estático con Nginx (PROD)
# ============================================================
FROM nginx:1.27-alpine AS runner

# Copiar el build de Vite
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
