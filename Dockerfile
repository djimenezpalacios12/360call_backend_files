# Usa una imagen base de Python ligera
FROM python:3.10-slim

# Instala herramientas de compilación necesarias
RUN apt-get update && \
    apt-get install -y build-essential && \
    # Instalar paquetes ICU para soporte de globalización "DESCOMENTAR LINEA DE ABAJO PARA SOLUCIONAR PROBLEMA ICU"
    apt-get install -y libicu-dev && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y instala las dependencias
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

# Copia el resto de la aplicación en el contenedor
COPY . .

# Establece el PYTHONPATH para que incluya el directorio /app
ENV PYTHONPATH=/app

# Expone el puerto en el que correrá la aplicación
EXPOSE 8001

# Comando para iniciar la aplicación con Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8001"]
