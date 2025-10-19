# Dockerfile

FROM python:3.12-slim

# Establece directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar algunas librerías y PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copia primero el archivo de requirements para usar cache de Docker
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto
COPY . .

# Expone puerto
EXPOSE 8000

# Comando por defecto (puede ser sobreescrito en docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
