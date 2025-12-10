import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.favorites.models import Favorites


async def create_favorite(session: AsyncSession, user_id: uuid.UUID, book_id: uuid.UUID) -> Favorites:
    favorite = Favorites(user_id=user_id, book_id=book_id)
    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)
    return favorite


async def get_favorite(session: AsyncSession, user_id: uuid.UUID, book_id: uuid.UUID) -> Favorites | None:
    result = await session.execute(select(Favorites).where(Favorites.user_id == user_id, Favorites.book_id == book_id))
    return result.scalars().first()


async def delete_favorite(session: AsyncSession, user_id: uuid.UUID, book_id: uuid.UUID) -> bool:
    favorite = await get_favorite(session, user_id, book_id)
    if not favorite:
        return False
    await session.delete(favorite)
    await session.commit()
    return True


async def list_favorites_by_user(session: AsyncSession, user_id: uuid.UUID) -> Sequence[Favorites]:
    result = await session.execute(select(Favorites).where(Favorites.user_id == user_id))
    return result.scalars().all()
