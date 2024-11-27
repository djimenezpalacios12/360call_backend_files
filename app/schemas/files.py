from typing import List
from pydantic import BaseModel


class IdArchivosOpenai(BaseModel):
    id_archivo: str
    nombre_documento: str
    id_area: str


class ArchivosUsuarioOpenai(BaseModel):
    file_id: str
    file_name: str
