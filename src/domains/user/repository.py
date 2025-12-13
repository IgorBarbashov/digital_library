import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domains.user.models import User
from src.exceptions.entity import EntityNotFound


async def get_user_orm_by_id(session: AsyncSession, user_id: uuid.UUID) -> User:
    stmt = select(User).options(selectinload(User.role)).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise EntityNotFound({"id": user_id}, entity_name="user")

    return user


async def get_user_orm_by_username(session: AsyncSession, username: str) -> User:
    stmt = select(User).options(selectinload(User.role)).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise EntityNotFound({"username": username}, entity_name="user")

    return user
