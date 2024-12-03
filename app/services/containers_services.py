from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from app.core.loggers.MyLogger import MyLogger
from app.core.storage_azure.containers_azure import (
    az_all_containers,
    az_remove_container,
)
from app.core.storage_azure.storage_azure import (
    az_new_contanier,
)
from app.schemas.response import ResponseModel


async def remove_container_services(
    container_name: str,
    request: Request,
    db: Session,
):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        all_containers = await az_remove_container(container_name)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=all_containers,
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")


async def all_containers_services(
    request: Request,
    db: Session,
):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        all_containers = await az_all_containers()

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=all_containers,
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")


async def create_container_services(
    container: str,
    request: Request,
    db: Session,
):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        container_created = await az_new_contanier(container)

        # Response
        response = ResponseModel(
            request_date=datetime.now(),
            message="success",
            code="200",
            data=container_created,
        )
        MyLogger.logger.info({"response": response})
        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exc:
        MyLogger.logger.error(f"error detail; {exc}")
        raise HTTPException(500, f"{exc}")
