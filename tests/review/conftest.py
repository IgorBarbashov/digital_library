import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.book.models import Book
from src.domains.genre.models import Genre
from src.domains.review.models import Review
from src.domains.user.models import User

TEST_GENRE_NAME = "Test Genre for Review"
TEST_BOOK_TITLE = "Test Book for Review"


@pytest_asyncio.fixture(scope="function")
async def test_genre(db_session: AsyncSession) -> Genre:
    result = await db_session.execute(
        select(Genre).where(Genre.name == TEST_GENRE_NAME)
    )
    genre = result.scalars().first()

    if genre is None:
        genre = Genre(name=TEST_GENRE_NAME)
        db_session.add(genre)
        await db_session.commit()

    return genre


@pytest_asyncio.fixture(scope="function")
async def test_book(db_session: AsyncSession, test_genre: Genre) -> Book:
    result = await db_session.execute(select(Book).where(Book.title == TEST_BOOK_TITLE))
    book = result.scalars().first()

    if book is None:
        book = Book(title=TEST_BOOK_TITLE, genre_id=test_genre.id)
        db_session.add(book)
        await db_session.commit()

    return book


@pytest_asyncio.fixture(scope="function")
async def test_review(
    db_session: AsyncSession, test_book: Book, existing_test_user: User
) -> Review:
    result = await db_session.execute(
        select(Review).where(
            Review.user_id == existing_test_user.id, Review.book_id == test_book.id
        )
    )
    review = result.scalars().first()

    if review is None:
        review = Review(
            user_id=existing_test_user.id,
            book_id=test_book.id,
            rating=5,
            text="Test review text",
        )
        db_session.add(review)
        await db_session.commit()

    return review
