import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.loggers.MyLogger import MyLogger

load_dotenv()
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DB = os.getenv("DATABASE_DB")
# Handle strings in password
DATABASE_PASSWORD_ESCAPED = quote_plus(DATABASE_PASSWORD)

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD_ESCAPED}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

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
                f"Successfully Connected to the database; {DATABASE_HOST}"
            )
    except Exception as exc:
        MyLogger.logger.error(f" Sorry Could not connect to the database: {exc}")
        return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
