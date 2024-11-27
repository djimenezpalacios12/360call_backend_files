from fastapi import HTTPException, UploadFile, status

from app.core.loggers.MyLogger import MyLogger

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()

mimetypes = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/csv",
    "text/plain",
    "application/pdf",
    # TODO: Descoment when transcripciòn function is ready
    # "audio/mpeg",
    # "audio/x-m4a",
]


def validate_mimetypes(file: UploadFile):
    try:
        if file.content_type is not mimetypes:
            return file
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file extension: {file.content_type}",
            )
    except Exception as exc:
        MyLogger.logger.error(f"Error en la carga de archivo: {exc}")
        return None
