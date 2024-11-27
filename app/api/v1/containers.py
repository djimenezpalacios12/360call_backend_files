from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.loggers.MyLogger import MyLogger
from app.services.containers_services import (
    all_containers_services,
    create_container_services,
    remove_container_services,
)

containersRouter = APIRouter()

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()


@containersRouter.post("/create/container/{container}")
async def create_container(
    container: str,  # Must be id_empresa
    request: Request,
    db: Session = Depends(get_db),
):
    return await create_container_services(container, request, db)


@containersRouter.get("/")
async def all_containers(
    request: Request,
    db: Session = Depends(get_db),
):
    return await all_containers_services(request, db)


@containersRouter.post("/remove/container/{container}")
async def remove_container(
    container: str,  # Must be id_empresa
    request: Request,
    db: Session = Depends(get_db),
):
    return await remove_container_services(container, request, db)
