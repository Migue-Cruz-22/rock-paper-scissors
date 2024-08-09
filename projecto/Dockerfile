# Usar la imagen base de Python
FROM python:3.11-slim

# Actualizar e instalar paquetes necesarios
RUN apt-get update \
    && apt-get install -y \
       python3-venv \
       sqlite3 \
       python3 \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos y el archivo principal
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates/ templates/

# Crear y activar un entorno virtual
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que la aplicación correrá
EXPOSE 5000

# Definir el comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
