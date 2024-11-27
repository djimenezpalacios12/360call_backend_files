from pydantic import BaseModel


class FileDownloadRequestName(BaseModel):
    file_name: str
