import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.db.base import connect
from app.core.loggers.MyLogger import MyLogger
from app.core.errors.errrors import register_all_errors
from app.middleware.isAdmin import isAdmin_middlware
from app.middleware.token_middleware import token_middleware_dependency
from app.api.v1.files import filesRouter
from app.api.v1.containers import containersRouter
from app.api.v1.filesAssistant import filesAssistantRouter

# Create FastAPI app instance
app = FastAPI(title="Backend FastAPI", version="0.0.1", description="MS Archivos")

# CORS middleware settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# Catch Errors
register_all_errors(app)

# Connect DB
connect()


# Routes
@app.get("/", tags=["Root"], include_in_schema=False)
def read_root() -> RedirectResponse:
    return RedirectResponse(url="/docs/")


app.include_router(
    filesRouter,
    prefix=f"/v1/api/files",
    tags=["files"],
    dependencies=[
        Depends(token_middleware_dependency),
    ],
)

app.include_router(
    containersRouter,
    prefix=f"/v1/api/containers",
    tags=["container"],
    dependencies=[Depends(token_middleware_dependency), Depends(isAdmin_middlware)],
)

app.include_router(
    filesAssistantRouter,
    prefix=f"/v1/api/assistants",
    tags=["Assistant"],
    dependencies=[Depends(token_middleware_dependency)],
)

# Main
if __name__ == "__main__":
    MyLogger.configure()
    MyLogger.logger.error("debug message")
    uvicorn.run(app, host="0.0.0.0", port=8001)
