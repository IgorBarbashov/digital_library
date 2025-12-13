
from fastapi import FastAPI

from src.api.v1.init import init_routers
from src.exceptions.init import init_exception_handlers

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

init_routers(app)
init_exception_handlers(app)
