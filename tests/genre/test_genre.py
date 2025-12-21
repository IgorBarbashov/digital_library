from typing import Any
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.genre.models import Genre
from src.domains.user.models import User
from tests.config import GENRE_API_BASE_URL


@pytest.mark.asyncio
async def test_get_all_genres(
    client: AsyncClient,
    test_genre: Genre,
) -> None:
    response = await client.get(GENRE_API_BASE_URL)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    genre_names = [genre["name"] for genre in data]
    assert test_genre.name in genre_names


@pytest.mark.asyncio
async def test_get_genre_by_id_success(
    client: AsyncClient,
    test_genre: Genre,
) -> None:
    response = await client.get(f"{GENRE_API_BASE_URL}{test_genre.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_genre.id)
    assert data["name"] == test_genre.name


@pytest.mark.asyncio
async def test_get_genre_by_id_not_found(
    client: AsyncClient,
) -> None:
    fake_id = uuid4()

    response = await client.get(f"{GENRE_API_BASE_URL}{fake_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_genre_by_id_validation_error(
    client: AsyncClient,
) -> None:
    response = await client.get(f"{GENRE_API_BASE_URL}not-a-uuid")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_genre_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_active_test_admin: User,
    admin_token: dict[str, Any],
) -> None:
    new_genre_name = "New Test Genre"

    result = await db_session.execute(select(Genre).where(Genre.name == new_genre_name))
    existing_genre = result.scalars().first()

    if existing_genre:
        await db_session.delete(existing_genre)
        await db_session.commit()

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": new_genre_name}
    response = await client.post(GENRE_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == new_genre_name
    assert "id" in data

    result = await db_session.execute(select(Genre).where(Genre.id == UUID(data["id"])))
    created_genre = result.scalars().first()
    assert created_genre is not None
    assert created_genre.name == new_genre_name


@pytest.mark.asyncio
async def test_create_genre_already_exists(
    client: AsyncClient,
    existing_active_test_admin: User,
    test_genre: Genre,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": test_genre.name}

    response = await client.post(GENRE_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_genre_validation_error(
    client: AsyncClient,
    existing_active_test_admin: User,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {}

    response = await client.post(GENRE_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_patch_genre_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_active_test_admin: User,
    test_genre: Genre,
    admin_token: dict[str, Any],
) -> None:
    updated_name = "Updated Genre Name"

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"name": updated_name}

    response = await client.patch(
        f"{GENRE_API_BASE_URL}{test_genre.id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_genre.id)
    assert data["name"] == updated_name

    result = await db_session.execute(select(Genre).where(Genre.id == test_genre.id))
    updated_genre = result.scalars().first()

    assert updated_genre is not None
    assert updated_genre.name == updated_name


@pytest.mark.asyncio
async def test_patch_genre_not_found(
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
        f"{GENRE_API_BASE_URL}{fake_id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_genre_validation_error(
    client: AsyncClient,
    existing_active_test_admin: User,
    test_genre: Genre,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.patch(
        f"{GENRE_API_BASE_URL}{test_genre.id}",
        headers=headers,
        json={},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_genre_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_active_test_admin: User,
    test_genre_2: Genre,
    admin_token: dict[str, Any],
) -> None:
    genre_id = test_genre_2.id

    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.delete(
        f"{GENRE_API_BASE_URL}{genre_id}",
        headers=headers,
    )

    assert response.status_code == 204

    result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
    deleted_genre = result.scalars().first()
    assert deleted_genre is None


@pytest.mark.asyncio
async def test_delete_genre_not_found(
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
        f"{GENRE_API_BASE_URL}{fake_id}",
        headers=headers,
    )

    assert response.status_code == 404
