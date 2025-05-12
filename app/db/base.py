import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.loggers.MyLogger import MyLogger

load_dotenv()
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
# Handle strings in password
DATABASE_PASSWORD_ESCAPED = quote_plus(POSTGRES_PASSWORD)

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{DATABASE_PASSWORD_ESCAPED}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

# Configura el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crea una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modelos
Base = declarative_base()


def get_connection():
    return engine

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def connect():
    try:
        with engine.connect() as conn:
            MyLogger.logger.info(
                f"Successfully Connected to the database; {POSTGRES_HOST}"
            )
    except Exception as exc:
        MyLogger.logger.error(f" Sorry Could not connect to the database: {exc}")
        return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
