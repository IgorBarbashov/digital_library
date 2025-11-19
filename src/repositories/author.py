import uuid
from typing import List, Optional, Union

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.db import get_async_session
from src.models.author import Author as AuthorOrm
from src.schemas.author import Author, AuthorWithGenre


class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> Union[List[Author], List[AuthorWithGenre]]:
        stmt = (
            select(AuthorOrm)
            .order_by(AuthorOrm.create_at.asc())
            .offset(skip)
            .limit(limit)
        )
        if with_genre:
            stmt = stmt.options(selectinload(AuthorOrm.genres))
        result = await self.db.execute(stmt)
        authors = result.scalars().all()

        return (
            [AuthorWithGenre.from_orm(author) for author in authors]
            if with_genre
            else [Author.from_orm(author) for author in authors]
        )

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Union[Optional[Author], Optional[AuthorWithGenre]]:
        stmt = select(AuthorOrm).where(AuthorOrm.id == author_id)
        if with_genre:
            stmt = stmt.options(selectinload(AuthorOrm.genres))
        result = await self.db.execute(stmt)
        author = result.scalar_one_or_none()

        if author is None:
            return None

        return (
            AuthorWithGenre.from_orm(author) if with_genre else Author.from_orm(author)
        )


async def get_author_repository(
    db: AsyncSession = Depends(get_async_session),
) -> AuthorRepository:
    return AuthorRepository(db)
