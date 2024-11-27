from typing import List
from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.schemas.files import ArchivosUsuarioOpenai, IdArchivosOpenai
from app.models.models import id_archivos_openai
from app.models.models import Area, id_archivos_openai


# Remove files (xlsx or csv)
async def remove_files(db: Session, id_files: List[str]):
    try:
        stmt = delete(id_archivos_openai).where(
            id_archivos_openai.id_archivo.in_(id_files)
        )
        db.execute(stmt)
        db.commit()

        return ""
    except HTTPException as exc:
        # HTTPException previa y la re-lanzamos
        db.rollback()
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registro no se puede eliminar de base de datos: {exc}",
        )


# Get user files (xlsx or csv)
async def get_id_files(db: Session, id_area: str):
    try:
        files = (
            db.query(id_archivos_openai)
            .filter(id_archivos_openai.id_area == id_area)
            .all()
        )

        print(files)
        filesResponse = []
        for file in files:
            fileResponse = ArchivosUsuarioOpenai(
                file_id=file.id_archivo,
                file_name=file.nombre_documento,
            )
            filesResponse.append(fileResponse)

        return filesResponse
    except HTTPException as exc:
        # HTTPException previa y la re-lanzamos
        db.rollback()
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registro no pude ser obtenido: {exc}",
        )


# Insert file (xlsx or csv)
async def save_id_file(db: Session, archivosOpenai: IdArchivosOpenai):
    try:
        # Prompt
        db_file = id_archivos_openai(**archivosOpenai.model_dump())
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file
    except HTTPException as exc:
        # HTTPException previa y la re-lanzamos
        db.rollback()
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registro no pude ser almacenado: {exc}",
        )
