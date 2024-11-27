from fastapi import APIRouter, Depends, Request, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.loggers.MyLogger import MyLogger
from app.schemas.request import FileDownloadRequestName
from app.services.files_services import (
    download_file_services,
    load_files_folder_services,
    load_files_services,
    remove_files_services,
    retrieve_files_services,
)

filesRouter = APIRouter()

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()


# Define el modelo del body


@filesRouter.post("/file/download")
async def download_file(
    body: FileDownloadRequestName,
    request: Request,
    db: Session = Depends(get_db),
):
    return await download_file_services(body, request, db)


# Load file in container/folder
@filesRouter.post("/load/folder")
async def load_files_folder(
    files: List[UploadFile],
    request: Request,
    db: Session = Depends(get_db),
):
    return await load_files_folder_services(files, request, db)


# Load file in container (general users)
@filesRouter.post("/load")
async def load_files(
    request: Request,
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(..., description="A list of files to be uploaded"),
):
    return await load_files_services(request, db, files)


@filesRouter.get("/")
async def retrieve_files(request: Request, db: Session = Depends(get_db)):
    return await retrieve_files_services(request, db)


@filesRouter.post("/remove")
async def remove_files(
    files: List[str], request: Request, db: Session = Depends(get_db)
):
    return await remove_files_services(files, request, db)
