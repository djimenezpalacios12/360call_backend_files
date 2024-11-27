from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


def register_all_errors(app: FastAPI):
    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Catch Internal Server Error!",
                "code": "500",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
