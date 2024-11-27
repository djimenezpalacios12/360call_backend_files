from pydantic import BaseModel


class TokenModel(BaseModel):
    _id: str
    correo: str
    rol: str
    nombre: str
    id_usuario: str
    iat: int
    exp: int
