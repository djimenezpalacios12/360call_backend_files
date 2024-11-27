from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.services.users_services import get_user
from app.core.loggers.MyLogger import MyLogger
from app.core.verify_access_token.token_validation import verify_access_token
from app.db.base import get_db

# Capturar el header Authorization
security = HTTPBearer()

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()


async def isAdmin_middlware(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        # Decodificamos el JWT
        payload = verify_access_token(request)
        user_response = get_user(db, user_id=payload["id_usuario"])

        if str(user_response.roles) == "usuario":
            MyLogger.logger.error("Usuario no autorizado")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no autorizado"
            )
        else:
            pass

    except HTTPException as exc:
        # HTTPException previa y la re-lanzamos
        raise exc
    except Exception as exc:
        # Para cualquier otro error que no sea HTTPException
        MyLogger.logger.error(f"Error inesperado: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error verifying token",
        )
