# ============================================================
# Stage 1: deps — instala dependencias (usado por dev con hot-reload)
# ============================================================
FROM node:20-alpine AS deps

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# ============================================================
# Stage 2: builder — compila el proyecto (usado en producción)
# ============================================================
FROM deps AS builder

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
