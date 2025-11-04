# src/api/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator

from src.utils.unitofwork import DefaultUnitOfWork, uow_factory


# Движок БД (в памяти — для тестов)
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
    future=True
)

# сессии
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# Depends для UoW
async def get_uow() -> AsyncGenerator[DefaultUnitOfWork, None]:
    async with uow_factory(AsyncSessionLocal) as uow:
        yield uow