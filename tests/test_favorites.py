import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.main import app
from src.setting import settings
from src.db.db import get_async_session
from src.domains.favorites.models import Favorites
from src.domains.user.models import User
from src.domains.book.models import Book
from src.domains.genre.models import Genre

TEST_DATABASE_URL = settings.db_dsn

engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        session = AsyncSessionLocal(bind=conn)
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session():
        return db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    user = User(
        username="testuser",
        first_name="Test",
        last_name="Testovich",
        email="test@example.com",
        disabled=False,
        hashed_password="fakehash",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_genre(db_session: AsyncSession) -> Genre:
    genre = Genre(name="Genre")
    db_session.add(genre)
    await db_session.commit()
    await db_session.refresh(genre)
    return genre


@pytest_asyncio.fixture
async def test_book(db_session: AsyncSession, test_genre: Genre) -> Book:
    book = Book(title="Test Book", author="Author A", genre_id=test_genre.id)
    db_session.add(book)
    await db_session.commit()
    await db_session.refresh(book)
    return book


@pytest.mark.asyncio
async def test_add_book_to_favorites(
    client: AsyncClient,
    test_user: User,
    test_book_with_genre: Book,
    test_genre: Genre,
):
    # Создаём избранное
    response = await client.post(
        "/favorites/",
        json={"book_id": str(test_book_with_genre.id)},
    )

    assert response.status_code == 201
    data = response.json()

    # Проверяем поля
    assert data["book_id"] == str(test_book_with_genre.id)
    assert "id" in data
    assert "user_id" in data

    # Дополнительно проверяем, что книга связана с корректным жанром
    assert "genre" in data["book"]  # если в схеме есть вложение genre
    assert data["book"]["genre"]["id"] == str(test_genre.id)
    assert data["book"]["genre"]["name"] == test_genre.name


@pytest.mark.asyncio
async def test_list_favorites_with_genres(
    client: AsyncClient,
    test_user: User,
    test_book_with_genre: Book,
    test_genre: Genre,
):
    # Добавляем книгу в избранное
    await client.post(
        "/favorites/",
        json={"book_id": str(test_book_with_genre.id)},
    )

    # Получаем список избранных
    response = await client.get("/favorites/")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    favorite = data[0]

    # Проверяем книгу и её жанр
    assert favorite["book"]["id"] == str(test_book_with_genre.id)
    assert favorite["book"]["title"] == test_book_with_genre.title
    assert favorite["book"]["genre"]["id"] == str(test_genre.id)
    assert favorite["book"]["genre"]["name"] == test_genre.name


@pytest.mark.asyncio
async def test_delete_favorite(
    client: AsyncClient,
    test_user: User,
    test_book_with_genre: Book,
    test_genre: Genre,
):
    # 1. Добавляем книгу в избранное
    response_add = await client.post(
        "/favorites/",
        json={"book_id": str(test_book_with_genre.id)},
    )
    assert response_add.status_code == 201
    favorite_id = response_add.json()["id"]

    # 2. Проверяем, что книга действительно в избранном
    response_list = await client.get("/favorites/")
    assert response_list.status_code == 200
    favorites = response_list.json()
    assert len(favorites) == 1
    assert favorites[0]["id"] == favorite_id
    assert favorites[0]["book"]["id"] == str(test_book_with_genre.id)

    # 3. Удаляем из избранного
    response_delete = await client.delete(f"/favorites/{favorite_id}")
    assert response_delete.status_code == 204  # No Content

    # 4. Проверяем, что запись исчезла
    response_list_after = await client.get("/favorites/")
    assert response_list_after.status_code == 200
    assert len(response_list_after.json()) == 0
