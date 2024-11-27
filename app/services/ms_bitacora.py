import os
from dotenv import load_dotenv
import httpx

from app.core.loggers.MyLogger import MyLogger

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()

load_dotenv()
API_MS_BITACORA = os.getenv("MS_BITACORA")


# Función para enviar la acción a la bitácora
def send_action_bitacora(token: str, action: str):

    headers = {"Authorization": f"bearer {token}"}
    data = {"accion": action}

    try:
        # Petición POST a la API de bitácora
        response = httpx.post(API_MS_BITACORA, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        # Loguear el error en caso de que ocurra
        MyLogger.logger.error(f"Error al enviar la acción a la bitácora: {exc}")
        return None
