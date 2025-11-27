from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.exceptions.entity import EntityNotFound, NoDataToUpdate


def init_exception_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFound)
    def entity_not_found_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    @app.exception_handler(NoDataToUpdate)
    def no_data_to_update_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )
