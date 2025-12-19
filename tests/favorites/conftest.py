import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.book.models import Book
from src.domains.genre.models import Genre

TEST_GENRE_NAME = "Test Genre"
TEST_BOOK_TITLE = "Test Book"


@pytest.fixture(scope="function")
async def test_genre(db_session: AsyncSession) -> Genre:
    result = await db_session.execute(select(Genre).where(Genre.name == TEST_GENRE_NAME))
    genre = result.scalars().first()

    if genre is None:
        genre = Genre(name=TEST_GENRE_NAME)
        db_session.add(genre)
        await db_session.commit()

    return genre


@pytest.fixture(scope="function")
async def test_book(db_session: AsyncSession, test_genre: Genre) -> Book:
    result = await db_session.execute(select(Book).where(Book.title == TEST_BOOK_TITLE))
    book = result.scalars().first()

    if book is None:
        book = Book(title=TEST_BOOK_TITLE, genre_id=test_genre.id)
        db_session.add(book)
        await db_session.commit()

    return book
