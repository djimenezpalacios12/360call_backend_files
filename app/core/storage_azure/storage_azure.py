import base64
from fastapi import File, HTTPException, UploadFile, status
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient

from app.core.azureOpenAI.azure_openai import client
from app.core.loggers.MyLogger import MyLogger
from app.core.storage_azure.containers_azure import az_new_contanier
from app.schemas.files import ArchivosUsuarioOpenai

load_dotenv()
if MyLogger.logger is None:
    MyLogger.configure()

AZURE_ACCOUNT_NAME_STORAGE = os.getenv("AZURE_ACCOUNT_NAME_STORAGE")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
STRING_CONNECT = f"DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME_STORAGE};AccountKey={AZURE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"


# * BLOB
# upload files (bytes) in container/folder
async def az_upload_files_bytes_folders(
    container_name: str,
    folder_name: str = None,
    fileName: str = "",
    fileBytes: bytes = None,
):
    try:
        MyLogger.logger.info(
            f"Subir archivo (bytes) a la carpeta de storage: ID {container_name}"
        )

        # Conectar con el servicio de Blob usando la cadena de conexión
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        container_client = blob_service_client.get_container_client(container_name)

        # Verificar si el contenedor existe
        if not container_client.exists():
            raise HTTPException(
                status_code=404, detail=f"El contenedor '{container_name}' no existe."
            )

        # Crear el nombre del blob incluyendo el nombre de la carpeta si se proporciona
        blob_name = f"{folder_name}/{fileName}"
        blob_client = container_client.get_blob_client(blob_name)

        # Leer y subir el archivo
        blob_client.upload_blob(fileBytes, overwrite=True)

        return {
            "mensaje": (
                f"Archivo '{fileName}' subido exitosamente a '{container_name}/{folder_name}'."
                if folder_name
                else f"Archivo '{fileName}' subido exitosamente a '{container_name}'."
            )
        }

    except Exception as e:
        MyLogger.logger.error(f"error detail; {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al subir el archivo: {str(e)}"
        )


# upload files in container/folder
async def az_upload_files_folders(
    container_name: str, folder_name: str = None, archivo: UploadFile = File(...)
):
    try:
        MyLogger.logger.info(
            f"Subir archivo (UploadFile) a la carpeta de storage: ID {container_name}"
        )

        # Conectar con el servicio de Blob usando la cadena de conexión
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        container_client = blob_service_client.get_container_client(container_name)

        # Verificar si el contenedor existe
        if not container_client.exists():
            await az_new_contanier(container_name)

        # Crear el nombre del blob incluyendo el nombre de la carpeta si se proporciona
        blob_name = (
            f"{folder_name}/{archivo.filename}" if folder_name else archivo.filename
        )
        blob_client = container_client.get_blob_client(blob_name)

        # Leer y subir el archivo
        contenido = await archivo.read()
        blob_client.upload_blob(contenido, overwrite=True)

        return {
            "mensaje": (
                f"Archivo '{archivo.filename}' subido exitosamente a '{container_name}/{folder_name}'."
                if folder_name
                else f"Archivo '{archivo.filename}' subido exitosamente a '{container_name}'."
            )
        }

    except Exception as e:
        MyLogger.logger.error(f"error detail; {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error al subir el archivo: {str(e)}"
        )


# upload files in container
async def az_upload_files(container_name: str, archivo: UploadFile = File(...)):
    try:
        # connect with Blob services
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        container_client = blob_service_client.get_container_client(container_name)

        # Check if the container exists
        if not container_client.exists():
            raise HTTPException(
                status_code=404, detail=f"El contenedor '{container_name}' no existe."
            )

        # Blob name
        blob_client = container_client.get_blob_client(archivo.filename)

        # Read and upload
        contenido = await archivo.read()
        blob_client.upload_blob(contenido, overwrite=True)

        return {
            "mensaje": f"Archivo '{archivo.filename}' subido exitosamente a'{container_name}'."
        }

    except Exception as e:
        MyLogger.logger.error(f"error detail; {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fail upload file: {str(e)}")


# Retrieve list files from storage
async def az_get_list_files(container_name: str):
    try:
        # Connect to storage account
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        container_client = blob_service_client.get_container_client(container_name)

        # Check if the container exists
        if not container_client.exists():
            raise HTTPException(
                status_code=404, detail=f"El contenedor '{container_name}' no existe."
            )

        # List all blobs in container
        blobs_list = container_client.list_blobs()
        archivos = [blob.name for blob in blobs_list]
        if not archivos:
            return {
                "mensaje": f"No se encontraron archivos en el contenedor '{container_name}'."
            }

        return archivos
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al listar los archivos: {str(e)}"
        )


# Delete file in storage
async def az_remove_file(container_name: str, file_name: str):
    try:
        # Connect to storage account
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        container_client = blob_service_client.get_container_client(container_name)

        # Check if the container exists
        if not container_client.exists():
            raise HTTPException(
                status_code=404, detail=f"El contenedor '{container_name}' no existe."
            )

        # ? Crear un cliente de Blob específico para el archivo
        blob_client = container_client.get_blob_client(file_name)

        # Verificar si el blob (archivo) existe
        if not blob_client.exists():
            raise HTTPException(
                status_code=404,
                detail=f"El archivo '{file_name}' no existe en el contenedor '{container_name}'.",
            )

        # delete blob
        blob_client.delete_blob()

        return {
            "mensaje": f"Archivo '{file_name}' eliminado exitosamente del contenedor '{container_name}'."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el archivo: {str(e)}"
        )


# Download file in storage
async def az_download_file(container_name: str, archivo_name: str):
    try:
        # Conectar con el servicio de Blob usando la cadena de conexión
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)

        # Obtener el cliente del contenedor
        container_client = blob_service_client.get_container_client(container_name)

        # Verificar si el contenedor existe
        if not container_client.exists():
            raise HTTPException(
                status_code=404, detail=f"El contenedor '{container_name}' no existe."
            )

        # Obtener el cliente del blob (archivo) que se quiere descargar
        blob_client = container_client.get_blob_client(archivo_name)

        # Verificar si el blob (archivo) existe
        if not blob_client.exists():
            raise HTTPException(
                status_code=404,
                detail=f"El archivo '{archivo_name}' no existe en el contenedor '{container_name}'.",
            )

        # Descargar el contenido del blob (archivo)
        stream = blob_client.download_blob()
        contenido = stream.readall()

        # Codificar el contenido en base64
        contenido_base64 = base64.b64encode(contenido).decode("utf-8")

        # Retornar el archivo en formato base64
        return {"archivo_base64": contenido_base64}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al descargar el archivo: {str(e)}"
        )
