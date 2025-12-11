from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.init import init_routers
from src.exceptions.init import init_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_routers(app)
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


init_exception_handlers(app)
