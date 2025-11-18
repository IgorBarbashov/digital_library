import uuid
from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.db import get_async_session
from src.models.author import Author


class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int, limit: int) -> Sequence[Author]:
        stmt = select(Author).order_by(Author.create_at.asc()).offset(skip).limit(limit)
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_all_with_genre(self, skip: int, limit: int) -> Sequence[Author]:
        stmt = (
            select(Author)
            .options(selectinload(Author.genres))
            .order_by(Author.create_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_by_id(self, author_id: uuid.UUID) -> Optional[Author]:
        stmt = select(Author).where(Author.id == author_id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()


async def get_author_repository(
    db: AsyncSession = Depends(get_async_session),
) -> AuthorRepository:
    return AuthorRepository(db)
