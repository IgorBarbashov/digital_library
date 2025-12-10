import asyncio
from contextlib import asynccontextmanager

from alembic.config import Config
from fastapi import FastAPI

from alembic import command
from src.api.v1.init import init_routers
from src.exceptions.init import init_exception_handlers
from src.setting import settings


async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.db_dsn)
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

#вынесен из lifespan, чтобы маршруты добавлялись до инициализации app
#это мешает тестам
init_routers(app) 

init_exception_handlers(app)
