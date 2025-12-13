from collections import defaultdict
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.domains.book.models import Book
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
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app), AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def existing_test_user(
    client: AsyncClient, db_session, test_user: dict[str, str] = TEST_USER
) -> dict[str, Any]:
    result = await db_session.execute(
        select(User).where(User.username == TEST_USER["username"])
    )
    user = result.scalars().first()
    await db_session.close()
    if user is None:
        user_headers = {"Content-Type": "application/json"}
        user_response = await client.post(
            "/api/v1/user/", headers=user_headers, json=test_user
        )
        return user_response.json()
    return {"id": str(user.id), "username": user.username, "email": user.email}


@pytest.fixture
async def user_token(
    client: AsyncClient, existing_test_user: dict[str, Any], test_user: dict[str, str] = TEST_USER
) -> dict[str, Any]:
    creds_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    creds_payload = {
        "username": test_user["username"],
        "password": test_user["password"],
    }
    creds_response = await client.post(
        "/api/v1/auth/login", headers=creds_headers, data=creds_payload
    )
    TEST_TOKEN["user_id"] = existing_test_user["id"]
    TEST_TOKEN["token"] = creds_response.json()
    return TEST_TOKEN


@pytest.fixture(scope="function")
async def test_book(db_session) -> Book:
    result = await db_session.execute(select(Book))
    book = result.scalars().first()
    return book


@pytest.mark.asyncio
async def test_get_all_reviews(client: AsyncClient):
    response = await client.get("/api/v1/review/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_review_by_invalid_uuid(client: AsyncClient):
    invalid_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/review/{invalid_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_review_by_malformed_uuid(client: AsyncClient):
    malformed_id = "not-a-uuid"
    response = await client.get(f"/api/v1/review/{malformed_id}")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_review_without_auth(client: AsyncClient):
    headers = {"Content-Type": "application/json"}
    review_payload = {
        "book_id": "00000000-0000-0000-0000-000000000000",
        "rating": 5,
        "text": "Great book!",
    }

    response = await client.post(
        "/api/v1/review/", headers=headers, json=review_payload
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_review_with_invalid_rating_low(
    client: AsyncClient, user_token: dict[str, Any]
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token['token']['access_token']}",
    }
    review_payload = {
        "book_id": "00000000-0000-0000-0000-000000000000",
        "rating": 0,
        "text": "Bad",
    }

    response = await client.post(
        "/api/v1/review/", headers=headers, json=review_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_review_with_invalid_rating_high(
    client: AsyncClient, user_token: dict[str, Any]
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token['token']['access_token']}",
    }
    review_payload = {
        "book_id": "00000000-0000-0000-0000-000000000000",
        "rating": 6,
        "text": "Too high",
    }

    response = await client.post(
        "/api/v1/review/", headers=headers, json=review_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_review_without_rating(
    client: AsyncClient, user_token: dict[str, Any]
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token['token']['access_token']}",
    }
    review_payload = {
        "book_id": "00000000-0000-0000-0000-000000000000",
        "text": "Missing rating",
    }

    response = await client.post(
        "/api/v1/review/", headers=headers, json=review_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_review_without_book_id(
    client: AsyncClient, user_token: dict[str, Any]
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token['token']['access_token']}",
    }
    review_payload = {"rating": 5, "text": "Missing book_id"}

    response = await client.post(
        "/api/v1/review/", headers=headers, json=review_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_patch_review_without_auth(client: AsyncClient):
    review_id = "00000000-0000-0000-0000-000000000000"
    headers = {"Content-Type": "application/json"}
    patch_payload = {"rating": 4}

    response = await client.patch(
        f"/api/v1/review/{review_id}", headers=headers, json=patch_payload
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_patch_review_with_invalid_rating(
    client: AsyncClient, user_token: dict[str, Any]
):
    review_id = "00000000-0000-0000-0000-000000000000"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token['token']['access_token']}",
    }
    patch_payload = {"rating": 10}

    response = await client.patch(
        f"/api/v1/review/{review_id}", headers=headers, json=patch_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_review_without_auth(client: AsyncClient):
    review_id = "00000000-0000-0000-0000-000000000000"

    response = await client.delete(f"/api/v1/review/{review_id}")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_review_with_auth(
    client: AsyncClient, user_token: dict[str, Any], test_book: Book
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token['token']['access_token']}",
    }
    review_payload = {
        "book_id": str(test_book.id),
        "rating": 5,
        "text": "Great book!",
    }

    response = await client.post(
        "/api/v1/review/", headers=headers, json=review_payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 5
    assert data["text"] == "Great book!"
    assert "id" in data
