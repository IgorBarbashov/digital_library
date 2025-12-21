from typing import Any
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.book.models import Book
from src.domains.review.models import Review
from src.domains.user.models import User
from tests.config import REVIEW_API_BASE_URL


@pytest.mark.asyncio
async def test_get_all_reviews(
    client: AsyncClient,
    test_review: Review,
) -> None:
    response = await client.get(REVIEW_API_BASE_URL)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_all_reviews_by_book_id(
    client: AsyncClient,
    test_review: Review,
    test_book: Book,
) -> None:
    response = await client.get(f"{REVIEW_API_BASE_URL}?book_id={test_book.id}")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert all(review["book_id"] == str(test_book.id) for review in data)


@pytest.mark.asyncio
async def test_get_review_by_id_success(
    client: AsyncClient,
    test_review: Review,
) -> None:
    response = await client.get(f"{REVIEW_API_BASE_URL}{test_review.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_review.id)
    assert data["rating"] == test_review.rating


@pytest.mark.asyncio
async def test_get_review_by_id_not_found(
    client: AsyncClient,
) -> None:
    fake_id = uuid4()

    response = await client.get(f"{REVIEW_API_BASE_URL}{fake_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_review_by_id_validation_error(
    client: AsyncClient,
) -> None:
    response = await client.get(f"{REVIEW_API_BASE_URL}not-a-uuid")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_review_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_test_user: User,
    test_book: Book,
    user_token: dict[str, Any],
) -> None:
    result = await db_session.execute(
        select(Review).where(
            Review.user_id == existing_test_user.id, Review.book_id == test_book.id
        )
    )
    existing_review = result.scalars().first()

    if existing_review:
        await db_session.delete(existing_review)
        await db_session.commit()

    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"book_id": str(test_book.id), "rating": 4, "text": "Great book!"}
    response = await client.post(REVIEW_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["book_id"] == str(test_book.id)
    assert data["rating"] == 4
    assert data["text"] == "Great book!"
    assert "id" in data

    result = await db_session.execute(
        select(Review).where(Review.id == UUID(data["id"]))
    )
    created_review = result.scalars().first()
    assert created_review is not None
    assert created_review.rating == 4


@pytest.mark.asyncio
async def test_create_review_unauthorized(
    client: AsyncClient,
    test_book: Book,
) -> None:
    payload = {"book_id": str(test_book.id), "rating": 4, "text": "Great book!"}

    response = await client.post(REVIEW_API_BASE_URL, json=payload)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_review_validation_error(
    client: AsyncClient,
    existing_test_user: User,
    user_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {}

    response = await client.post(REVIEW_API_BASE_URL, headers=headers, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_patch_review_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_test_user: User,
    test_review: Review,
    user_token: dict[str, Any],
) -> None:
    updated_rating = 3
    updated_text = "Updated review text"

    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"rating": updated_rating, "text": updated_text}

    response = await client.patch(
        f"{REVIEW_API_BASE_URL}{test_review.id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_review.id)
    assert data["rating"] == updated_rating
    assert data["text"] == updated_text

    result = await db_session.execute(select(Review).where(Review.id == test_review.id))
    updated_review = result.scalars().first()

    assert updated_review is not None
    assert updated_review.rating == updated_rating
    assert updated_review.text == updated_text


@pytest.mark.asyncio
async def test_patch_review_unauthorized(
    client: AsyncClient,
    test_review: Review,
) -> None:
    payload = {"rating": 3}

    response = await client.patch(
        f"{REVIEW_API_BASE_URL}{test_review.id}",
        json=payload,
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_patch_review_forbidden(
    client: AsyncClient,
    test_review: Review,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"rating": 3}

    response = await client.patch(
        f"{REVIEW_API_BASE_URL}{test_review.id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_patch_review_not_found(
    client: AsyncClient,
    existing_test_user: User,
    user_token: dict[str, Any],
) -> None:
    fake_id = uuid4()

    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }
    payload = {"rating": 3}

    response = await client.patch(
        f"{REVIEW_API_BASE_URL}{fake_id}",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_review_success(
    client: AsyncClient,
    db_session: AsyncSession,
    existing_test_user: User,
    test_review: Review,
    user_token: dict[str, Any],
) -> None:
    review_id = test_review.id

    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.delete(
        f"{REVIEW_API_BASE_URL}{review_id}",
        headers=headers,
    )

    assert response.status_code == 204

    result = await db_session.execute(select(Review).where(Review.id == review_id))
    deleted_review = result.scalars().first()
    assert deleted_review is None


@pytest.mark.asyncio
async def test_delete_review_unauthorized(
    client: AsyncClient,
    test_review: Review,
) -> None:
    response = await client.delete(
        f"{REVIEW_API_BASE_URL}{test_review.id}",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_review_forbidden(
    client: AsyncClient,
    test_review: Review,
    admin_token: dict[str, Any],
) -> None:
    headers = {
        "Authorization": f"Bearer {admin_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.delete(
        f"{REVIEW_API_BASE_URL}{test_review.id}",
        headers=headers,
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_review_not_found(
    client: AsyncClient,
    existing_test_user: User,
    user_token: dict[str, Any],
) -> None:
    fake_id = uuid4()

    headers = {
        "Authorization": f"Bearer {user_token['token']['access_token']}",
        "Content-Type": "application/json",
    }

    response = await client.delete(
        f"{REVIEW_API_BASE_URL}{fake_id}",
        headers=headers,
    )

    assert response.status_code == 404
