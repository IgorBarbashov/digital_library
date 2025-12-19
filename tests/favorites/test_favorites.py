from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.book.models import Book
from src.domains.favorites.models import Favorites
from tests.config import FAVORIYES_API_BASE_URL


@pytest.mark.asyncio
async def test_add_book_to_favorites(
    client: AsyncClient, db_session: AsyncSession, user_token: dict[str, Any], test_book: Book
) -> None:
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

    response = await client.post(FAVORIYES_API_BASE_URL, headers=headers, json=favorites_payload)

    assert response.status_code == 201

    data = response.json()

    assert data["book_id"] == str(test_book.id)
    assert "user_id" in data
