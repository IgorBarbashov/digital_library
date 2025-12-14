import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.domains.book.repository import (
    create_book,
    delete_book,
    get_book_by_id,
    get_book_information,
    get_books_list,
    update_book,
)
from src.domains.book.schema import (
    BookCreateSchema,
    BookFilters,
    BookInformationSchema,
    BookReadSchema,
    BookUpdateSchema,
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_book_handler(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    book: BookCreateSchema,
) -> BookReadSchema:
    return await create_book(session, book)


@router.get("/{id}")
async def get_book_handler(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: uuid.UUID,
) -> BookReadSchema:
    return await get_book_by_id(session, id)


@router.get("/")
async def books_list_handler(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    filters: Annotated[BookFilters, Depends()],
) -> list[BookReadSchema]:
    return await get_books_list(session, filters)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book_handler(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: uuid.UUID,
):
    await delete_book(session, id)


@router.patch("/{id}")
async def patch_book_handler(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: uuid.UUID,
    book: BookUpdateSchema,
) -> BookReadSchema:
    return await update_book(session, id, book)


@router.get("/{id}/information")
async def get_book_information_handler(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: uuid.UUID,
) -> BookInformationSchema:
    result = await get_book_information(session, id)
    return BookInformationSchema.model_validate(result)
