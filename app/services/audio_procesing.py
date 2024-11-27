from fastapi import HTTPException, status

from app.core.loggers.MyLogger import MyLogger


if MyLogger.logger is None:
    MyLogger.configure()


async def process_audio():
    try:
        # ...
        return "success"
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        MyLogger.logger.error(f"Error en transcripcion de audio: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en transcripcion de audio: {exc}",
        )
