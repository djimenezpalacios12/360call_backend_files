from typing import Any
from pydantic import BaseModel

# Esquemas para validar la entrada y salida de datos


class UsuariosBase(BaseModel):
    id_usuario: str
    nombre: str
    correo: str
    rol: Any


class UsuariosAreaData(BaseModel):
    id_usuario: str
    id_area: str
    asistente: str
    vectores: str
