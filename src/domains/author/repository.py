import uuid
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.db import get_async_session
from src.domains.author.entity import AuthorEntity
from src.domains.author.models import Author
from src.domains.author.protocols import AuthorRepository
from src.domains.author.schema import AuthorMappers
from src.domains.common.association.author_genre import AuthorGenre


class AuthorRepositoryPG(AuthorRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> List[AuthorEntity]:
        stmt = select(Author).order_by(Author.create_at.asc()).offset(skip).limit(limit)
        if with_genre:
            stmt = stmt.options(selectinload(Author.genres))
        result = await self.db.execute(stmt)
        authors = result.scalars().all()

        return AuthorMappers.orm_to_entity_list(authors, with_genre)

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Optional[AuthorEntity]:
        author = await self.get_by_id_orm(author_id, with_genre)
        if author is None:
            return None

        return AuthorMappers.orm_to_entity(author, with_genre)

    async def create(self, author: AuthorEntity) -> AuthorEntity:
        author_orm = AuthorMappers.entity_to_orm(author)
        self.db.add(author_orm)
        await self.db.flush()

        for genre_id in author.genres:
            author_genre = AuthorGenre(author_id=author_orm.id, genre_id=genre_id)
            self.db.add(author_genre)

        await self.db.commit()

        created_author = await self.get_by_id(author_orm.id, with_genre=True)
        assert created_author is not None
        return created_author

    async def update(
        self, author_id: uuid.UUID, author: dict
    ) -> Optional[AuthorEntity]:
        author_orm = await self.get_by_id_orm(author_id, with_genre=True)
        if not author_orm:
            return None

        genres_ids = author.pop("genres", None)

        for key, value in author.items():
            setattr(author_orm, key, value)
        await self.db.flush()

        if genres_ids is not None:
            await self.db.execute(
                delete(AuthorGenre).where(AuthorGenre.author_id == author_id)
            )

            for genre_id in genres_ids:
                author_genre = AuthorGenre(author_id=author_id, genre_id=genre_id)
                self.db.add(author_genre)

        await self.db.commit()
        await self.db.refresh(author_orm)

        return AuthorMappers.orm_to_entity(author_orm, with_genre=True)

    async def delete(self, author_id: uuid.UUID) -> bool:
        author = await self.get_by_id_orm(author_id, with_genre=False)

        if author:
            await self.db.delete(author)
            await self.db.commit()
            return True

        return False

    async def get_by_id_orm(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Optional[Author]:
        stmt = select(Author).where(Author.id == author_id)
        if with_genre:
            stmt = stmt.options(selectinload(Author.genres))
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()


async def get_author_repository(
    db: AsyncSession = Depends(get_async_session),
) -> AuthorRepository:
    return AuthorRepositoryPG(db)
