import uuid
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy import CursorResult, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.db import get_async_session
from src.domains.author.models import Author
from src.domains.author.repository import get_author_orm_by_id
from src.domains.author.schema import AuthorCreateSchema, AuthorPatchSchema, AuthorReadSchema
from src.domains.common.association.author_genre import AuthorGenre
from src.exceptions.entity import EntityNotFound

router = APIRouter()


@router.get(
    "/",
    summary="Получить список авторов",
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    with_genre: Annotated[bool, Query(..., description="Загружать ли жанры")] = False,
) -> list[AuthorReadSchema]:
    stmt = select(Author).order_by(Author.create_at.asc())
    if with_genre:
        stmt = stmt.options(selectinload(Author.genres))
    result = await session.execute(stmt)
    authors = result.scalars().all()

    return [AuthorReadSchema.from_orm_with_genres(author, with_genre) for author in authors]


@router.get(
    "/{author_id}",
    summary="Получить автора по id",
)
async def get_by_id(
    author_id: Annotated[uuid.UUID, Path(..., description="ID автора")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    with_genre: Annotated[bool, Query(..., description="Загружать ли жанры")] = False,
) -> AuthorReadSchema:
    author = await get_author_orm_by_id(session, author_id, with_genre)
    return AuthorReadSchema.from_orm_with_genres(author, with_genre)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать автора",
)
async def create_author(
    author_data: AuthorCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthorReadSchema:
    author = Author(**author_data.model_dump(exclude={"genres"}))
    session.add(author)
    await session.flush()

    for genre_id in author_data.genres:
        author_genre = AuthorGenre(author_id=author.id, genre_id=genre_id)
        session.add(author_genre)

    await session.commit()

    created_author = await get_author_orm_by_id(session, author.id, with_genre=True)
    return AuthorReadSchema.from_orm_with_genres(created_author, with_genre=True)


@router.patch(
    "/{author_id}",
    summary="Частичное обновление автора",
)
async def patch_author(
    author_data: AuthorPatchSchema,
    author_id: Annotated[uuid.UUID, Path(..., description="ID автора")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthorReadSchema:
    update_data = author_data.model_dump(exclude_unset=True)
    genres_ids = update_data.pop("genres", None)

    stmt = update(Author).where(Author.id == author_id).values(**update_data)
    result = await session.execute(stmt)
    cursor_result = cast(CursorResult, result)

    if cursor_result.rowcount == 0:
        raise EntityNotFound({"id": author_id}, entity_name="author")

    await session.flush()

    if genres_ids is not None:
        await session.execute(delete(AuthorGenre).where(AuthorGenre.author_id == author_id))

        for genre_id in genres_ids:
            author_genre = AuthorGenre(author_id=author_id, genre_id=genre_id)
            session.add(author_genre)

    await session.commit()

    updated_author = await get_author_orm_by_id(session, author_id, with_genre=True)
    return AuthorReadSchema.from_orm_with_genres(updated_author, with_genre=True)


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить автора по id",
)
async def delete_author(
    author_id: Annotated[uuid.UUID, Path(..., description="ID автора")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    stmt = delete(Author).where(Author.id == author_id).returning(Author.id)
    result = await session.execute(stmt)
    deleted_ids = [row[0] for row in result]

    if not deleted_ids:
        raise EntityNotFound({"id": author_id}, entity_name="author")

    await session.commit()
