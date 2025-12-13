from collections import defaultdict
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.domains.category.models import Category
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

TEST_ADMIN = {
    "username": "adminuser123",
    "first_name": "Admin",
    "last_name": "User",
    "email": "adminuser123@example.com",
    "disabled": "false",
    "password": "AdminPass123!",
    "role": "admin",
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
async def existing_test_admin(
    client: AsyncClient, db_session, test_admin: dict[str, str] = TEST_ADMIN
) -> User:
    result = await db_session.execute(
        select(User).where(User.username == TEST_ADMIN["username"])
    )
    user = result.scalars().first()
    await db_session.close()
    if user is None:
        user_headers = {"Content-Type": "application/json"}
        user_response = await client.post(
            "/api/v1/user/", headers=user_headers, json=test_admin
        )
        return user_response.json()
    return user


@pytest.fixture
async def admin_token(
    client: AsyncClient,
    existing_test_admin: User,
    test_admin: dict[str, str] = TEST_ADMIN,
) -> dict[str, Any]:
    creds_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    creds_payload = {
        "username": test_admin["username"],
        "password": test_admin["password"],
    }
    creds_response = await client.post(
        "/api/v1/auth/login", headers=creds_headers, data=creds_payload
    )
    TEST_TOKEN["admin_id"] = existing_test_admin.id
    TEST_TOKEN["token"] = creds_response.json()
    return TEST_TOKEN


@pytest.fixture(scope="function")
async def test_category(db_session) -> Category:
    result = await db_session.execute(
        select(Category).where(Category.name == "Test Category")
    )
    category = result.scalars().first()
    if category is None:
        category = Category(name="Test Category")
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
    return category


@pytest.mark.asyncio
async def test_get_all_categories(client: AsyncClient):
    response = await client.get("/api/v1/category/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_category_by_invalid_uuid(client: AsyncClient):
    invalid_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/category/{invalid_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_category_by_malformed_uuid(client: AsyncClient):
    malformed_id = "not-a-uuid"
    response = await client.get(f"/api/v1/category/{malformed_id}")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_category_without_auth(client: AsyncClient):
    headers = {"Content-Type": "application/json"}
    category_payload = {"name": "Test Category"}

    response = await client.post(
        "/api/v1/category/", headers=headers, json=category_payload
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_category_with_empty_name(client: AsyncClient):
    headers = {"Content-Type": "application/json"}
    category_payload = {"name": ""}

    response = await client.post(
        "/api/v1/category/", headers=headers, json=category_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_category_with_long_name(client: AsyncClient):
    headers = {"Content-Type": "application/json"}
    category_payload = {"name": "a" * 101}

    response = await client.post(
        "/api/v1/category/", headers=headers, json=category_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_category_without_name(client: AsyncClient):
    headers = {"Content-Type": "application/json"}
    category_payload = {}

    response = await client.post(
        "/api/v1/category/", headers=headers, json=category_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_patch_category_without_auth(client: AsyncClient):
    category_id = "00000000-0000-0000-0000-000000000000"
    headers = {"Content-Type": "application/json"}
    patch_payload = {"name": "Updated Name"}

    response = await client.patch(
        f"/api/v1/category/{category_id}", headers=headers, json=patch_payload
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_patch_category_with_empty_name(client: AsyncClient):
    category_id = "00000000-0000-0000-0000-000000000000"
    headers = {"Content-Type": "application/json"}
    patch_payload = {"name": ""}

    response = await client.patch(
        f"/api/v1/category/{category_id}", headers=headers, json=patch_payload
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_category_without_auth(client: AsyncClient):
    category_id = "00000000-0000-0000-0000-000000000000"

    response = await client.delete(f"/api/v1/category/{category_id}")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_category_with_admin(
    client: AsyncClient, admin_token: dict[str, Any]
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
    }
    category_payload = {"name": "New Category Test"}

    response = await client.post(
        "/api/v1/category/", headers=headers, json=category_payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Category Test"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_category_by_id(client: AsyncClient, test_category: Category):
    response = await client.get(f"/api/v1/category/{test_category.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_category.id)
    assert data["name"] == test_category.name
