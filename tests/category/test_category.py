from typing import Any
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.category.models import Category
from src.domains.user.models import User
from tests.config import CATEGORY_API_BASE_URL


@pytest.mark.asyncio
async def test_get_all_categories(
    client: AsyncClient,
    test_category: Category,
) -> None:
    response = await client.get(CATEGORY_API_BASE_URL)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    category_names = [category["name"] for category in data]
    assert test_category.name in category_names


@pytest.mark.asyncio
async def test_get_category_by_id_success(
    client: AsyncClient,
    test_category: Category,
) -> None:
    response = await client.get(f"{CATEGORY_API_BASE_URL}{test_category.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_category.id)
    assert data["name"] == test_category.name


@pytest.mark.asyncio
async def test_get_category_by_id_not_found(
    client: AsyncClient,
) -> None:
    fake_id = uuid4()

    response = await client.get(f"{CATEGORY_API_BASE_URL}{fake_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_category_by_id_validation_error(
    client: AsyncClient,
) -> None:
    response = await client.get(f"{CATEGORY_API_BASE_URL}not-a-uuid")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_category_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_active_test_admin: User,
    admin_token: dict[str, Any],
) -> None:
    new_category_name = "New Test Category"

    result = await db_session.execute(
        select(Category).where(Category.name == new_category_name)
    )
    existing_category = result.scalars().first()

    if existing_category:
        await db_session.delete(existing_category)
        await db_session.commit()

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": new_category_name}
    response = await client.post(CATEGORY_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == new_category_name
    assert "id" in data

    result = await db_session.execute(
        select(Category).where(Category.id == UUID(data["id"]))
    )
    created_category = result.scalars().first()
    assert created_category is not None
    assert created_category.name == new_category_name


@pytest.mark.asyncio
async def test_create_category_already_exists(
    client: AsyncClient,
    existing_active_test_admin: User,
    test_category: Category,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": test_category.name}

    response = await client.post(CATEGORY_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_category_unauthorized(
    client: AsyncClient,
) -> None:
    payload = {"name": "Test Category"}

    response = await client.post(CATEGORY_API_BASE_URL, json=payload)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_category_forbidden(
    client: AsyncClient,
    user_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": "Test Category"}

    response = await client.post(CATEGORY_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_category_validation_error(
    client: AsyncClient,
    existing_active_test_admin: User,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {}

    response = await client.post(CATEGORY_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_patch_category_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_active_test_admin: User,
    test_category: Category,
    admin_token: dict[str, Any],
) -> None:
    updated_name = "Updated Category Name"

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": updated_name}

    response = await client.patch(
        f"{CATEGORY_API_BASE_URL}{test_category.id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_category.id)
    assert data["name"] == updated_name

    result = await db_session.execute(
        select(Category).where(Category.id == test_category.id)
    )
    updated_category = result.scalars().first()

    assert updated_category is not None
    assert updated_category.name == updated_name


@pytest.mark.asyncio
async def test_patch_category_unauthorized(
    client: AsyncClient,
    test_category: Category,
) -> None:
    payload = {"name": "Updated Name"}

    response = await client.patch(
        f"{CATEGORY_API_BASE_URL}{test_category.id}",
        json=payload,
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_patch_category_forbidden(
    client: AsyncClient,
    test_category: Category,
    user_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": "Updated Name"}

    response = await client.patch(
        f"{CATEGORY_API_BASE_URL}{test_category.id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_patch_category_not_found(
    client: AsyncClient,
    existing_active_test_admin: User,
    admin_token: dict[str, Any],
) -> None:
    fake_id = uuid4()

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": "Some Name"}

    response = await client.patch(
        f"{CATEGORY_API_BASE_URL}{fake_id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_category_already_exists(
    client: AsyncClient,
    existing_active_test_admin: User,
    test_category: Category,
    test_category_2: Category,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": test_category_2.name}

    response = await client.patch(
        f"{CATEGORY_API_BASE_URL}{test_category.id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_delete_category_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_active_test_admin: User,
    test_category_2: Category,
    admin_token: dict[str, Any],
) -> None:
    category_id = test_category_2.id

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.delete(
        f"{CATEGORY_API_BASE_URL}{category_id}",
        headers=headers,
    )

    assert response.status_code == 204

    result = await db_session.execute(
        select(Category).where(Category.id == category_id)
    )
    deleted_category = result.scalars().first()
    assert deleted_category is None


@pytest.mark.asyncio
async def test_delete_category_unauthorized(
    client: AsyncClient,
    test_category: Category,
) -> None:
    response = await client.delete(
        f"{CATEGORY_API_BASE_URL}{test_category.id}",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_category_forbidden(
    client: AsyncClient,
    test_category: Category,
    user_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.delete(
        f"{CATEGORY_API_BASE_URL}{test_category.id}",
        headers=headers,
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_category_not_found(
    client: AsyncClient,
    existing_active_test_admin: User,
    admin_token: dict[str, Any],
) -> None:
    fake_id = uuid4()

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.delete(
        f"{CATEGORY_API_BASE_URL}{fake_id}",
        headers=headers,
    )

    assert response.status_code == 404
