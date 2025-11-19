from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.exceptions.entity import EntityNotFound


def init_exception_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFound)
    def entity_not_found_handler(request, exc) -> JSONResponse:
        """Обработчик исключений EntityNotFound."""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )
