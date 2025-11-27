import uuid
from typing import List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.domains.genre.models import Genre
from src.domains.genre.schema import (
    GenreCreateSchema,
    GenreReadSchema,
    GenreUpdateSchema,
)
from src.exceptions.entity import EntityAlreadyExists, EntityNotFound

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
        raise EntityNotFound(genre_id, entity_name="genre")

    return GenreReadSchema.model_validate(genre)


@router.post(
    "/",
    response_model=GenreReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать жанр",
)
async def create_genre(
    genre_data: GenreCreateSchema,
    session: AsyncSession = Depends(get_async_session),
) -> GenreReadSchema:
    stmt = select(Genre).where(Genre.name == genre_data.name)
    result = await session.scalars(stmt)
    existing_genre = result.first()

    if existing_genre:
        raise EntityAlreadyExists(id=existing_genre.id, entity_name="genre")

    genre = Genre(name=genre_data.name)
    session.add(genre)

    await session.commit()
    await session.refresh(genre)

    return GenreReadSchema.model_validate(genre)


@router.put(
    "/{genre_id}",
    response_model=GenreReadSchema,
    summary="Обновить жанр",
)
async def update_genre(
    genre_data: GenreUpdateSchema,
    genre_id: uuid.UUID = Path(..., description="ID жанра"),
    session: AsyncSession = Depends(get_async_session),
) -> GenreReadSchema:
    genre = await session.get(Genre, genre_id)

    if not genre:
        EntityNotFound(genre_id, "genre")

    update_data = genre_data.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(genre, k, v)

    session.add(genre)
    await session.commit()
    await session.refresh(genre)

    return GenreReadSchema.model_validate(genre)


@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить жанр по id",
)
async def delete_genre(
    genre_id: uuid.UUID = Path(..., description="ID жанра"),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    genre = await session.get(Genre, genre_id)

    if not genre:
        raise EntityNotFound(genre_id, entity_name="genre")

    await session.delete(genre)
    await session.commit()
