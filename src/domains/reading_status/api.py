import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy import and_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.guards import get_current_active_user
from src.db.db import get_async_session
from src.domains.book.constants import ORDER_COLUMN_MAP
from src.domains.book.models import Book
from src.domains.book.schema import BookWithReadingStatusReadSchema
from src.domains.reading_status.models import ReadingStatus
from src.domains.reading_status.schema import (
    ReadingStatusCreateSchema,
    ReadingStatusFiltersSchema,
    ReadingStatusOrderSchema,
    ReadingStatusPathSchema,
    ReadingStatusReadSchema,
)
from src.domains.user.schema import UserReadSchema
from src.exceptions.entity import EntityAlreadyExists, EntityNotFound
from src.utils.request_builder import apply_ordering

router = APIRouter(prefix="/book")


@router.get(
    "/",
    summary="Получить список книг текущего пользователя со статусом чтения",
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    filters: Annotated[ReadingStatusFiltersSchema, Depends()],
    order: Annotated[ReadingStatusOrderSchema, Depends()],
) -> list[BookWithReadingStatusReadSchema]:
    stmt = select(Book, ReadingStatus.status).join(ReadingStatus).where(ReadingStatus.user_id == current_user.id)
    stmt = apply_ordering(stmt, order, ORDER_COLUMN_MAP)

    if filters.status:
        stmt = stmt.where(ReadingStatus.status == filters.status)

    result = await session.execute(stmt)
    books = result.all()

    return [BookWithReadingStatusReadSchema.from_orm_with_status(book, status) for book, status in books]


@router.get(
    "/{book_id}/reading-status",
    summary="Получить статус чтения книги текущего пользователя",
)
async def get_reading_status(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    book_id: Annotated[uuid.UUID, Path(..., description="ID книги")],
) -> ReadingStatusReadSchema:
    stmt = select(ReadingStatus).where(
        and_(
            ReadingStatus.user_id == current_user.id,
            ReadingStatus.book_id == book_id,
        )
    )

    result = await session.execute(stmt)
    status = result.scalar_one_or_none()

    if status is None:
        raise EntityNotFound({"reading_status for book_id": book_id}, entity_name="reading_status")

    return ReadingStatusReadSchema.from_orm(status)


@router.post(
    "/reading-status",
    status_code=status.HTTP_201_CREATED,
    summary="Установить статус чтения книги для текущего пользователя",
)
async def set_reading_status(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    reading_status_data: ReadingStatusCreateSchema,
) -> None:
    status = ReadingStatus(
        user_id=current_user.id,
        **reading_status_data.model_dump(),
    )

    session.add(status)

    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        msg = str(getattr(err, "orig", err))

        if "uc_user_book" in msg:
            raise EntityAlreadyExists(
                {"user_id": current_user.id, "book_id": reading_status_data.book_id},
                entity_name="reading_status",
            ) from None

        if "reading_status_book_id_fkey" in msg:
            raise EntityNotFound(
                {"id": reading_status_data.book_id},
                entity_name="book",
            ) from None


@router.patch(
    "/reading-status",
    summary="Обновить статус чтения книги для текущего пользователя",
)
async def patch_reading_status(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    reading_status_data: ReadingStatusPathSchema,
) -> ReadingStatusReadSchema:
    stmt = (
        update(ReadingStatus)
        .where(
            and_(
                ReadingStatus.user_id == current_user.id,
                ReadingStatus.book_id == reading_status_data.book_id,
            )
        )
        .values({"status": reading_status_data.status})
        .returning(ReadingStatus)
    )

    result = await session.execute(stmt)
    status = result.scalar_one_or_none()

    if status is None:
        raise EntityNotFound({"reading_status for book_id": reading_status_data.book_id}, entity_name="reading_status")

    await session.commit()

    return ReadingStatusReadSchema.model_validate(status)
