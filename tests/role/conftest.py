import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.role.models import Role

ROLES = ["user", "admin"]


@pytest.fixture(scope="function", autouse=True)
async def seed_roles(db_session: AsyncSession) -> None:
    for name in ROLES:
        result = await db_session.execute(select(Role).where(Role.name == name))
        role = result.scalars().first()

        if role is None:
            db_session.add(Role(name=name))

    await db_session.commit()
