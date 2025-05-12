from fastapi import File, HTTPException, status
from dotenv import load_dotenv
import os

from app.core.azureOpenAI.azure_openai import client
from app.core.loggers.MyLogger import MyLogger
from app.schemas.files import ArchivosUsuarioOpenai

load_dotenv()
if MyLogger.logger is None:
    MyLogger.configure()

AZURE_ACCOUNT_NAME_STORAGE = os.getenv("AZURE_ACCOUNT_NAME_STORAGE")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
STRING_CONNECT = f"DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME_STORAGE};AccountKey={AZURE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"


# upload files in vectore store assistant
async def az_assis_upload_file(
    asistente: str,
    vectores: str,
    file_location: str,
):
    try:
        # Update Vector with new files
        MyLogger.logger.info(
            f"Upload File at Assistant {asistente} in vector store {vectores}"
        )

        # Upload File to Assistant
        fileData = open(file_location, "rb")
        file = client.files.create(file=fileData, purpose="assistants")

        # Remove temp file
        fileData.close()
        os.remove(file_location)

        MyLogger.logger.info(f"File processed successfully: {file.id}")

        # update vector with id file prev. uploaded
        file = client.beta.vector_stores.files.create_and_poll(
            vector_store_id=vectores, file_id=file.id
        )

        return {"content": "success"}
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        MyLogger.logger.error(f"Error carga en Azure: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error carga en Azure: {exc}",
        )


# Upload Excel or csv
async def az_assis_excel_upload(file_location: str):
    try:
        # Send file to openAI
        fileData = open(file_location, "rb")
        file = client.files.create(file=fileData, purpose="assistants")

        # Remove temp file
        fileData.close()
        os.remove(file_location)

        return file.id
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        MyLogger.logger.error(f"Error carga en Azure: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error carga en Azure: {exc}",
        )


# remove files from assistant
async def az_assis_remove_file(vectores: str, file: ArchivosUsuarioOpenai):
    try:
        file_ext = file.file_name.split(".")[-1]
        if file_ext == "xlsx" or file_ext == "csv":
            client.files.delete(file.file_id)
        else:
            deleted_vector_store_file = client.beta.vector_stores.files.delete(
                vector_store_id=vectores, file_id=file.file_id
            )
            if hasattr(deleted_vector_store_file, "id"):
                client.files.delete(file.file_id)

        return "Archivos Eliminados"
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        MyLogger.logger.error(f"Error al obtener listado: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener listado: {exc}",
        )


# retrieve list documents
async def az_assis_retrieve_file(id_vector: str):
    try:
        document_names = []

        vector_store_files = client.beta.vector_stores.files.list(
            vector_store_id=id_vector
        )

        for file in vector_store_files.data:
            fileid = file.id
            filename = client.files.retrieve(fileid)
            document_names.append({"file_id": fileid, "file_name": filename.filename})

        return document_names
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        MyLogger.logger.error(f"Error al obtener listado: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener listado: {exc}",
        )
