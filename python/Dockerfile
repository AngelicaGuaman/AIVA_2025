FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar código
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip && pip install -e .

# Entrypoint opcional (si lo vas a usar como ejecutable)
CMD ["python", "main.py"]
