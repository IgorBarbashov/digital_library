import asyncio
from contextlib import asynccontextmanager

from alembic.config import Config
from fastapi import FastAPI

from alembic import command
from src.api.v1.author import router as author_router
from src.setting import settings


async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.db_dsn)
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await run_migrations()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, world!"}


app.include_router(author_router, prefix="/api/v1/author", tags=["author"])
