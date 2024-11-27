from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from app.core.verify_access_token.token_validation import verify_access_token
from app.core.loggers.MyLogger import MyLogger

# Capturar el header Authorization
security = HTTPBearer()

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()

async def token_middleware_dependency(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    try:
        # Decodificamos el JWT
        verify_access_token(request)
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
