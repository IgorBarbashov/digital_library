import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.category.models import Category

TEST_CATEGORY_NAME = "Test Category"
TEST_CATEGORY_NAME_2 = "Test Category 2"


@pytest_asyncio.fixture(scope="function")
async def test_category(db_session: AsyncSession) -> Category:
    result = await db_session.execute(
        select(Category).where(Category.name == TEST_CATEGORY_NAME)
    )
    category = result.scalars().first()

    if category is None:
        category = Category(name=TEST_CATEGORY_NAME)
        db_session.add(category)
        await db_session.commit()

    return category


@pytest_asyncio.fixture(scope="function")
async def test_category_2(db_session: AsyncSession) -> Category:
    result = await db_session.execute(
        select(Category).where(Category.name == TEST_CATEGORY_NAME_2)
    )
    category = result.scalars().first()

    if category is None:
        category = Category(name=TEST_CATEGORY_NAME_2)
        db_session.add(category)
        await db_session.commit()

    return category
