import os
import jwt
from fastapi import HTTPException

from app.core.loggers.MyLogger import MyLogger

# Setting/init logger
if MyLogger.logger is None:
    MyLogger.configure()

# Define the algorithm used for JWT encoding/decoding.
# Retrieve the secret key and algorithm from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


def verify_access_token(request):
    try:
        # Retrieve token from header
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        # Decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        # Raise an HTTPException with status code 401 if the token has expired
        MyLogger.logger.error("Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        # Raise an HTTPException with status code 401 if the token is invalid
        MyLogger.logger.error("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")
