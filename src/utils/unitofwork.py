# src/utils/unitofwork.py
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Any
from sqlalchemy.ext.asyncio import AsyncSession


#  Интерфейс UoW (абстрактный класс)
class AbstractUnitOfWork(ABC):
    session: AsyncSession

    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork":
        ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


#  Реализация UoW (без репозиториев)
class DefaultUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory
        self.session: AsyncSession

    async def __aenter__(self) -> "DefaultUnitOfWork":
        self.session = self.session_factory()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


# Depends
@asynccontextmanager
async def uow_factory(
    session_factory: Callable[[], AsyncSession]
) -> AsyncGenerator[DefaultUnitOfWork, None]:
    uow = DefaultUnitOfWork(session_factory)
    async with uow:
        yield uow