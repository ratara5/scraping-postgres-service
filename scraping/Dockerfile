FROM python:3.8-slim

# Install neccesary dependences
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
    # Clean cache in order to reduce image size

# Copy whole content from project to container, including requirements.txt
COPY . /app

# Indicate working directory
WORKDIR /app

# Add directory to path
ENV PYTHONPATH="/app"

# Install python dependences
RUN pip install --no-cache-dir -r requirements.txt

# Default command (optional)