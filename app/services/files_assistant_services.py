import os
from fastapi import HTTPException, Request, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
import base64

from app.core.loggers.MyLogger import MyLogger
from app.core.storage_azure.storage_azure import (
    az_assis_excel_upload,
    az_assis_remove_file,
    az_assis_retrieve_file,
    az_assis_upload_file,
    az_upload_files_folders,
)
from app.core.verify_access_token.token_validation import verify_access_token
from app.schemas.files import ArchivosUsuarioOpenai, IdArchivosOpenai
from app.schemas.response import ResponseModel
from app.services.audio_procesing import process_audio
from app.services.company_services import get_user_empresa
from app.services.mime_types import validate_mimetypes
from app.services.queries_services import get_id_files, remove_files, save_id_file
from app.services.users_services import get_user_area


# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()

# Settings for create temp. folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print("Directory created successfully!")
else:
    print("Directory already exists!")


# remove files from assistant services
async def remove_files_assistant_services(
    request: Request, files: List[ArchivosUsuarioOpenai], db: Session
):
    try:
        # retrieve data user
        payload = verify_access_token(request)
        user_id = payload["id_usuario"]
        user_data_response = get_user_area(db, user_id)
        vectores = user_data_response.vectores

        # remove files from assistant
        for file in files:
            # Delete assistant
            await az_assis_remove_file(vectores, file)
            # Delete registers if .xlsx o .csv
            await remove_files(db, [file.file_id])

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data="Registros eliminados",
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        MyLogger.logger.error(f"Error inesperado: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {exc}",
        )


# get list files in assistant
async def get_files_assistant_services(
    request: Request,
    db: Session,
):
    try:
        # Get user info.
        payload = verify_access_token(request)
        user_id = payload["id_usuario"]
        user_area_data = get_user_area(db, user_id)

        filesDocuments = await az_assis_retrieve_file(user_area_data.vectores)
        filesCodeInterpreter = await get_id_files(db, user_area_data.id_area)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=filesDocuments + filesCodeInterpreter,
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        MyLogger.logger.error(f"Error inesperado: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {exc}",
        )


# upload files in assistant
async def upload_files_assistant_services(
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
        user_id = payload["id_usuario"]
        id_empresa = get_user_empresa(db, user_id)  # container name
        user_area_data = get_user_area(db, user_id)

        # Validate MimeTypes
        files_success = list(map(lambda file: validate_mimetypes(file), files))
        files_success_cleaned = list(
            filter(lambda file: file is not None, files_success)
        )

        # load every file
        for file in files_success_cleaned:
            content_audio = "audio/mpeg"
            content_csv = "text/csv"
            content_sheet = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            unique_filename = file.filename
            file_bytes = file.file.read()
            file_location = f"{UPLOAD_FOLDER}/{unique_filename}"

            # 1. Audio
            if file.content_type == content_audio:
                with open(file_location, "wb+") as file_object:
                    file_object.write(file_bytes)
                await process_audio(file_location)

                # Save in AZ assis. y Storage.
                file_location_txt = file_location + ".txt"
                MyLogger.logger.info(f"Subiendo archivo en {file_location}")
                await az_assis_upload_file(
                    user_area_data.asistente,
                    user_area_data.vectores,
                    file_location_txt,
                )
                await az_upload_files_folders(id_empresa, user_id, file)
                os.remove(file_location)

            # 2. Spreadsheet
            elif file.content_type == content_csv or file.content_type == content_sheet:
                # Save data from file in a Temp. file
                with open(file_location, "wb+") as file_object:
                    file_object.write(file_bytes)

                file_id = await az_assis_excel_upload(file_location)
                MyLogger.logger.info(f"Subiendo archivo en {file_location}")
                await az_upload_files_folders(id_empresa, user_id, file)
                new_colection_prompt_object = IdArchivosOpenai(
                    id_archivo=file_id,
                    nombre_documento=unique_filename,
                    id_area=user_area_data.id_area,
                )
                await save_id_file(db, new_colection_prompt_object)

            # 3. Other Docs
            else:
                MyLogger.logger.info(f"Subiendo documento")
                # Save data from file in a Temp. file
                with open(file_location, "wb+") as file_object:
                    file_object.write(file_bytes)
                # Save in AZ assis. y Storage.
                MyLogger.logger.info(f"Subiendo archivo en {file_location}")
                await az_assis_upload_file(
                    user_area_data.asistente, user_area_data.vectores, file_location
                )
                await az_upload_files_folders(id_empresa, user_id, file)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data="success",
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        os.remove(file_location)
        os.remove(file_location + ".txt")
        MyLogger.logger.error(f"Error inesperado: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {exc}",
        )
