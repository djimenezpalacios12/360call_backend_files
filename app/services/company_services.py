from sqlalchemy.orm import Session

from app.models.models import Usuarios, Area


def get_user_empresa(db: Session, user_id=str):
    ex = db.query(Usuarios).filter(Usuarios.id_usuario == user_id).first()
    return ex.id_empresa
