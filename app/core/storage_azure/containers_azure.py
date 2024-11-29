from fastapi import HTTPException
from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

from app.core.loggers.MyLogger import MyLogger

load_dotenv()
if MyLogger.logger is None:
    MyLogger.configure()

ACCOUNT_NAME_STORAGE = os.getenv("ACCOUNT_NAME_STORAGE")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")
STRING_CONNECT = f"DefaultEndpointsProtocol=https;AccountName={ACCOUNT_NAME_STORAGE};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"


# Remove specific container
async def az_remove_container(container_name: str):
    try:
        # Conectar con el servicio de Blob usando la cadena de conexión
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        container_client = blob_service_client.get_container_client(container_name)

        # Verificar si el contenedor existe antes de intentar eliminarlo
        if not container_client.exists():
            raise HTTPException(
                status_code=404, detail=f"El contenedor '{container_name}' no existe."
            )

        # Eliminar el contenedor
        container_client.delete_container()

        return {
            "mensaje": f"El contenedor '{container_name}' ha sido eliminado exitosamente."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el contenedor: {str(e)}"
        )


# List all container
async def az_all_containers():
    try:
        # Conectar con el servicio de Blob usando la cadena de conexión
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        containers_list = blob_service_client.list_containers()

        # Extraer los nombres de los contenedores
        contenedores = [container.name for container in containers_list]
        if not contenedores:
            return {
                "mensaje": "No se encontraron contenedores en la cuenta de almacenamiento."
            }

        return {"contenedores": contenedores}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al listar los contenedores: {str(e)}"
        )


# Create new container in storage azure account
async def az_new_contanier(container_name: str):
    try:
        # Conecta con el servicio de Blob
        blob_service_client = BlobServiceClient.from_connection_string(STRING_CONNECT)
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()

        return {"mensaje": f"Contenedor '{container_name}' creado exitosamente."}
    except ResourceExistsError:
        MyLogger.logger.error(f"El contenedor '{container_name}' ya existe.")
        raise HTTPException(
            status_code=400, detail=f"El contenedor '{container_name}' ya existe."
        )
    except Exception as e:
        MyLogger.logger.error(f"error detail; {e}")
        raise HTTPException(
            status_code=500, detail=f"Error al crear el contenedor: {str(e)}"
        )
