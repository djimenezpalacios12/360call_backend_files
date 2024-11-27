from sqlalchemy.orm import Session

from app.models.models import Area, Usuarios
from app.schemas.schemas import UsuariosAreaData


def get_user(db: Session, user_id: int):
    return db.query(Usuarios).filter(Usuarios.id_usuario == user_id).first()


def get_user_area(db: Session, user_id: int):
    usuario, area = (
        db.query(Usuarios, Area)
        .join(Area, Usuarios.id_area == Area.id_area)
        .filter(Usuarios.id_usuario == user_id)
        .first()
    )

    queryResponse = UsuariosAreaData(
        id_usuario=usuario.id_usuario,
        id_area=area.id_area,
        asistente=area.asistente,
        vectores=area.vectores,
    )
    return queryResponse
