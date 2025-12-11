from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.exceptions.auth import AdminRoleRequired, BadCredentials, InactiveUser, IncorrectUsernamePassword
from src.exceptions.entity import EntityAlreadyExists, EntityIntegrityException, EntityNotFound, NoDataToPatchEntity


def init_exception_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFound)
    def entity_not_found_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    @app.exception_handler(EntityAlreadyExists)
    def entity_already_exists_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": exc.message},
        )

    @app.exception_handler(NoDataToPatchEntity)
    def no_data_to_patch_entity_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(InactiveUser)
    def inactive_user_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.message},
        )

    @app.exception_handler(BadCredentials)
    @app.exception_handler(IncorrectUsernamePassword)
    def bad_credentials_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": exc.message},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(AdminRoleRequired)
    def admin_role_required_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": exc.message},
        )

    @app.exception_handler(EntityIntegrityException)
    async def db_integrity_handler(request: Request, exc: EntityIntegrityException):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Entity integrity error",
                "detail": exc.detail,
            },
        )
