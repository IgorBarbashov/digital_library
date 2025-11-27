import uuid
from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.domains.genre.models import Genre
from src.domains.genre.schema import GenreReadSchema
from src.exceptions.entity import EntityNotFound

router = APIRouter()


@router.get(
    "/",
    response_model=List[GenreReadSchema],
    summary="Получить список жанров",
)
async def get_all(
    session: AsyncSession = Depends(get_async_session),
) -> List[GenreReadSchema]:
    stmt = select(Genre).order_by(Genre.create_at.asc())
    result = await session.execute(stmt)
    genres = result.scalars().all()

    return [GenreReadSchema.model_validate(genre) for genre in genres]


@router.get(
    "/{genre_id}",
    response_model=GenreReadSchema,
    summary="Получить жанр по id",
)
async def get_by_id(
    genre_id: uuid.UUID = Path(..., description="ID жанра"),
    session: AsyncSession = Depends(get_async_session),
) -> GenreReadSchema:
    genre = await session.get(Genre, genre_id)

    if not genre:
        raise EntityNotFound(genre_id, name="genre")

    return GenreReadSchema.model_validate(genre)
