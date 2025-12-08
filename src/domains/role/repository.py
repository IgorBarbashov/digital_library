from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.user_role import UserRole
from src.domains.role.models import Role
from src.exceptions.entity import EntityNotFound


async def get_role_orm_by_name(session: AsyncSession, role_name: UserRole) -> Role:
    stmt = select(Role).where(Role.name == role_name.value)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if role is None:
        raise EntityNotFound({"name": role_name}, "role")

    return role
