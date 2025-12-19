from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.user.models import User
from tests.config import AUTH_API_BASE_URL, USER_API_BASE_URL

TEST_USER = {
    "username": "testuser123",
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser123@example.com",
    "disabled": "false",
    "password": "StrongPass123!",
    "role": "user",
}


@pytest.fixture(scope="function")
async def existing_test_user(
    client: AsyncClient, db_session: AsyncSession, test_user: dict[str, str] = TEST_USER
) -> User:
    result = await db_session.execute(select(User).where(User.username == test_user["username"]))
    user = result.scalars().first()

    if user is None:
        user_headers = {"Content-Type": "application/json"}
        user_response = await client.post(USER_API_BASE_URL, headers=user_headers, json=test_user)
        assert user_response.status_code == 201

        result = await db_session.execute(select(User).where(User.username == test_user["username"]))
        user = result.scalars().first()
        assert user is not None, "User created via API but not found in DB"

    return user


@pytest.fixture
async def user_token(
    client: AsyncClient, existing_test_user: User, test_user: dict[str, str] = TEST_USER
) -> dict[str, Any]:
    creds_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    creds_payload = {"username": test_user["username"], "password": test_user["password"]}
    creds_response = await client.post(f"{AUTH_API_BASE_URL}login", headers=creds_headers, data=creds_payload)
    assert creds_response.status_code == 200

    token = creds_response.json()

    return {
        "user_id": existing_test_user.id,
        "token": token,
    }
