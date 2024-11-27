from fastapi import HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from app.core.loggers.MyLogger import MyLogger
from app.core.verify_access_token.token_validation import verify_access_token
from app.core.storage_azure.storage_azure import (
    az_download_file,
    az_get_list_files,
    az_remove_file,
    az_upload_files,
    az_upload_files_folders,
)
from app.schemas.response import ResponseModel
from app.services.company_services import get_user_empresa
from app.services.mime_types import validate_mimetypes

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()


async def download_file_services(
    body: str,
    request: Request,
    db: Session,
):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        # Get user info.
        payload = verify_access_token(request)
        user_id = payload["id_usuario"]
        id_empresa = get_user_empresa(db, user_id)

        contenido = await az_download_file(id_empresa, body.file_name)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=contenido,
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")


async def load_files_folder_services(
    files: List[UploadFile],
    request: Request,
    db: Session,
):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        # Get user info.
        payload = verify_access_token(request)
        user_id = payload["id_usuario"]  # folder name
        id_empresa = get_user_empresa(db, user_id)  # container name

        # Validate MimeTypes
        files_success = list(map(lambda file: validate_mimetypes(file), files))
        files_success_cleaned = list(
            filter(lambda file: file is not None, files_success)
        )

        # Upload in AZ
        for file in files_success_cleaned:
            await az_upload_files_folders(id_empresa, user_id, file)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=f"Archivos cargados con éxito",
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")


async def load_files_services(
    request: Request,
    db: Session,
    files: List[UploadFile],
):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        # Get user info.
        payload = verify_access_token(request)
        user_id = payload["id_usuario"]
        id_empresa = get_user_empresa(db, user_id)

        # Validate MimeTypes
        files_success = list(map(lambda file: validate_mimetypes(file), files))
        files_success_cleaned = list(
            filter(lambda file: file is not None, files_success)
        )

        # Upload in AZ
        for file in files_success_cleaned:
            await az_upload_files(id_empresa, file)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=f"Archivos cargados con éxito",
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")


async def retrieve_files_services(
    request: Request,
    db: Session,
):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        # Get user info.
        payload = verify_access_token(request)
        user_id = payload["id_usuario"]
        id_empresa = get_user_empresa(db, user_id)

        list_files = await az_get_list_files(id_empresa)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=list_files,
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")


async def remove_files_services(files: List[str], request: Request, db: Session):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        # Get user info.
        payload = verify_access_token(request)
        user_id = payload["id_usuario"]
        id_empresa = get_user_empresa(db, user_id)

        for file in files:
            await az_remove_file(id_empresa, file)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data="Archivos removidos",
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")
