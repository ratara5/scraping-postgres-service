FROM python:3.8-slim

# Instalar dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    iputils-ping \
    wget \
    gnupg \
    curl \
    
    # libnss3 \
    # libxss1 \
    # libgconf-2-4 \
    # libx11-xcb1 \
    # libxi6 \
    # libxtst6 \
    
    chromium \

    # chromium-driver \

    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  
    # Limpieza de caché para reducir el tamaño de la imagen

# Copiar todo el contenido del proyecto al contenedor, incluido requirements.txt
COPY . /app

# Establecer el directorio de trabajo
WORKDIR /app

# Agregar directorio a path
ENV PYTHONPATH="/app"

# Instalar las dependencias de Python usando pip
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto (opcional)