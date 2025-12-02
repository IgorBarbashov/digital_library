import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domains.author.models import Author
from src.exceptions.entity import EntityNotFound


async def get_author_orm_by_id(
    session: AsyncSession, author_id: uuid.UUID, with_genre: bool
) -> Author:
    stmt = select(Author).where(Author.id == author_id)
    if with_genre:
        stmt = stmt.options(selectinload(Author.genres))
    result = await session.execute(stmt)
    author = result.scalar_one_or_none()

    if author is None:
        raise EntityNotFound({"id": author_id}, entity_name="author")

    return author
