from collections import defaultdict
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.domains.book.models import Book
from src.domains.favorites.models import Favorites
from src.domains.genre.models import Genre
from src.domains.user.models import User
from src.main import app
from src.setting import settings

TEST_DATABASE_URL = settings.db_dsn


TEST_USER = {
    "username": "testuser123",
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser123@example.com",
    "disabled": "false",
    "password": "StrongPass123!",
    "role": "user",
}


TEST_TOKEN = defaultdict()

async_engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)


@pytest.fixture
async def db_session():
    async with async_sessionmaker(async_engine, expire_on_commit=False)() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture
def client() -> AsyncClient:
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    return client


@pytest.fixture(scope="function")
async def existing_test_user(client: AsyncClient, db_session, test_user: dict[str, str] = TEST_USER) -> User:
    result = await db_session.execute(select(User).where(User.username == TEST_USER["username"]))
    user = result.scalars().first()
    await db_session.close()
    if user is None:
        user_headers = {"Content-Type": "application/json"}
        user_response = await client.post("/api/v1/user/", headers=user_headers, json=test_user)
        return user_response.json()
    return user


@pytest.fixture
async def user_token(
    client: AsyncClient, existing_test_user: User, test_user: dict[str, str] = TEST_USER
) -> dict[str, Any]:
    creds_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    creds_payload = {"username": test_user["username"], "password": test_user["password"]}
    creds_response = await client.post("/api/v1/auth/login", headers=creds_headers, data=creds_payload)
    TEST_TOKEN["user_id"] = existing_test_user.id
    TEST_TOKEN["token"] = creds_response.json()
    return TEST_TOKEN


@pytest.fixture(scope="function")
async def test_genre(db_session) -> Genre:
    result = await db_session.execute(select(Genre).where(Genre.name == "Genre"))
    genre = result.scalars().first()
    if genre is None:
        genre = Genre(name="Genre")
        db_session.add(genre)
        await db_session.commit()
        await db_session.refresh(genre)
    return genre


@pytest.fixture(scope="function")
async def test_book(db_session, test_genre: Genre) -> Book:
    result = await db_session.execute(select(Book).where(Book.title == "Test Book"))
    book = result.scalars().first()
    if book is None:
        book = Book(title="Test Book11", genre_id=test_genre.id)
        db_session.add(book)
        await db_session.commit()
        await db_session.refresh(book)
    return book


# @pytest.mark.asyncio
# async def test_client_with_token(client: AsyncClient, user_token: dict[str, Any]):
#     headers = {
#         "Authorization": f"Bearer {user_token['token']['access_token']}",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     response = await client.get("/api/v1/user/me", headers=headers)

#     assert response.status_code == 201
#     data = response.json()
#     assert data["user_id"] == user_token["user"].id


@pytest.mark.asyncio
async def test_add_book_to_favorites(client: AsyncClient, db_session, user_token: dict[str, Any], test_book: Book):
    result = await db_session.execute(
        select(Favorites).where(Favorites.user_id == user_token["user_id"], Favorites.book_id == test_book.id)
    )
    favorites = result.scalars().first()

    if favorites:
        await db_session.delete(favorites)
        await db_session.commit()

    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    favorites_payload = {"user_id": str(user_token["user_id"]), "book_id": str(test_book.id)}

    response = await client.post(
        "/api/v1/favorites/",
        headers=headers,
        json=favorites_payload,
    )

    assert response.status_code == 201

    data = response.json()
    print(data)
    assert data["book_id"] == str(test_book.id)
    assert "user_id" in data


# @pytest.mark.asyncio
# async def test_list_favorites(client: AsyncClient):
#     headers = {
#         "Authorization": f"Bearer {TEST_TOKEN['token']['access_token']}",
#         "Content-Type": "application/json"
#     }

#     response = await client.get("/api/v1/favorites/", headers=headers)
#     assert response.status_code == 200
#     print(response)
    
#     data = response.json()

#     assert len(data) == 1
#     favorite = data[0]
#     print(favorite)


# @pytest.mark.asyncio
# async def test_delete_favorite(client: AsyncClient, user_token: dict[str, Any], test_book: Book):
#     headers = {
#         "Authorization": f"Bearer {user_token['token']['access_token']}",
#         "Content-Type": "application/json",
#     }

#     response_delete = await client.delete(f"/api/v1/favorites/{test_book.id}", headers=headers)
#     assert response_delete.status_code == 204  # No Content
