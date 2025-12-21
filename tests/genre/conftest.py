import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.genre.models import Genre

TEST_GENRE_NAME = "Test Genre"
TEST_GENRE_NAME_2 = "Test Genre 2"


@pytest_asyncio.fixture(scope="function")
async def test_genre(db_session: AsyncSession) -> Genre:
    result = await db_session.execute(select(Genre).where(Genre.name == TEST_GENRE_NAME))
    genre = result.scalars().first()

    if genre is None:
        genre = Genre(name=TEST_GENRE_NAME)
        db_session.add(genre)
        await db_session.commit()

    return genre


@pytest_asyncio.fixture(scope="function")
async def test_genre_2(db_session: AsyncSession) -> Genre:
    result = await db_session.execute(select(Genre).where(Genre.name == TEST_GENRE_NAME_2))
    genre = result.scalars().first()

    if genre is None:
        genre = Genre(name=TEST_GENRE_NAME_2)
        db_session.add(genre)
        await db_session.commit()

    return genre
