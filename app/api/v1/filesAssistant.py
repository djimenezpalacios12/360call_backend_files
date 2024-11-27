from fastapi import APIRouter, Depends, Request, UploadFile
from typing import List
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.loggers.MyLogger import MyLogger
from app.schemas.files import ArchivosUsuarioOpenai
from app.services.files_assistant_services import (
    get_files_assistant_services,
    remove_files_assistant_services,
    upload_files_assistant_services,
)


filesAssistantRouter = APIRouter()

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()


# Upload files assistant
@filesAssistantRouter.post("/files")
async def upload_files_assistant(
    files: List[UploadFile],
    request: Request,
    db: Session = Depends(get_db),
):
    return await upload_files_assistant_services(files, request, db)


# Get files assistant
@filesAssistantRouter.get("/files")
async def get_files_assistant(
    request: Request,
    db: Session = Depends(get_db),
):
    return await get_files_assistant_services(request, db)


# Remove files assistant
@filesAssistantRouter.post("/files/remove")
async def remove_files_assistant(
    request: Request,
    files: List[ArchivosUsuarioOpenai],
    db: Session = Depends(get_db),
):
    return await remove_files_assistant_services(request, files, db)
