# ============================================================
# Backend — FastAPI + uvicorn
# ============================================================
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para grpcio y similares
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python primero (mejor cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY app/ app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
