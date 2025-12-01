import uuid
from typing import List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.domains.genre.models import Genre
from src.domains.genre.schema import (
    GenreCreateSchema,
    GenrePatchSchema,
    GenreReadSchema,
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

    if genre is None:
        raise EntityNotFound({"id": genre_id}, entity_name="genre")

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
    genre = Genre(name=genre_data.name)
    session.add(genre)

    try:
        await session.commit()
        return GenreReadSchema.model_validate(genre)

    except IntegrityError as err:
        await session.rollback()

        if "UNIQUE" in str(err.orig):
            raise EntityAlreadyExists({"name": genre_data.name}, entity_name="genre")

        raise


@router.patch(
    "/{genre_id}",
    response_model=GenreReadSchema,
    summary="Частичное обновление жанра",
)
async def patch_genre(
    genre_data: GenrePatchSchema,
    genre_id: uuid.UUID = Path(..., description="ID жанра"),
    session: AsyncSession = Depends(get_async_session),
) -> GenreReadSchema:
    update_data = genre_data.model_dump(exclude_unset=True)

    stmt = (
        update(Genre).where(Genre.id == genre_id).values(**update_data).returning(Genre)
    )
    result = await session.execute(stmt)
    updated_genre = result.scalar_one_or_none()

    if updated_genre is None:
        raise EntityNotFound({"id": genre_id}, entity_name="genre")

    await session.commit()

    return GenreReadSchema.model_validate(updated_genre)


@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить жанр по id",
)
async def delete_genre(
    genre_id: uuid.UUID = Path(..., description="ID жанра"),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    stmt = delete(Genre).where(Genre.id == genre_id).returning(Genre.id)
    result = await session.execute(stmt)
    deleted_ids = [row[0] for row in result]

    if not deleted_ids:
        raise EntityNotFound({"id": genre_id}, entity_name="genre")

    await session.commit()
