from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class ResponseModel(BaseModel):
    request_date: datetime
    message: str
    code: str
    data: Optional[Any]
