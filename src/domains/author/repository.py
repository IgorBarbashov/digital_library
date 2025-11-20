import uuid
from typing import List, Optional, Union

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.db import get_async_session
from src.domains.author.models import Author
from src.domains.author.protocols import AuthorRepository
from src.domains.author.schema import AuthorSchema, AuthorWithGenreSchema


class AuthorRepositoryPG(AuthorRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> Union[List[AuthorSchema], List[AuthorWithGenreSchema]]:
        stmt = select(Author).order_by(Author.create_at.asc()).offset(skip).limit(limit)
        if with_genre:
            stmt = stmt.options(selectinload(Author.genres))
        result = await self.db.execute(stmt)
        authors = result.scalars().all()

        return (
            [AuthorWithGenreSchema.from_orm(author) for author in authors]
            if with_genre
            else [AuthorSchema.from_orm(author) for author in authors]
        )

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Union[Optional[AuthorSchema], Optional[AuthorWithGenreSchema]]:
        stmt = select(Author).where(Author.id == author_id)
        if with_genre:
            stmt = stmt.options(selectinload(Author.genres))
        result = await self.db.execute(stmt)
        author = result.scalar_one_or_none()

        if author is None:
            return None

        return (
            AuthorWithGenreSchema.from_orm(author)
            if with_genre
            else AuthorSchema.from_orm(author)
        )


async def get_author_repository(
    db: AsyncSession = Depends(get_async_session),
) -> AuthorRepository:
    return AuthorRepositoryPG(db)
