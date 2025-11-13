from contextlib import asynccontextmanager

from alembic.config import Config
from fastapi import FastAPI

from alembic import command
from src.setting import settings


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.alembic_db_dsn)
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    run_migrations()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, world!"}
