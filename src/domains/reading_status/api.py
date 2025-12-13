from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.guards import get_current_active_user
from src.db.db import get_async_session
from src.domains.book.constants import ORDER_COLUMN_MAP
from src.domains.book.models import Book
from src.domains.book.schema import BookReadSchema
from src.domains.reading_status.models import ReadingStatus
from src.domains.reading_status.schema import ReadingStatusFiltersSchema, ReadingStatusOrderSchema
from src.domains.user.schema import UserReadSchema
from src.utils.request_builder import apply_ordering

router = APIRouter(prefix="/books")


@router.get(
    "/",
    summary="Получить список книг текущего пользователя",
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    filters: Annotated[ReadingStatusFiltersSchema, Depends()],
    order: Annotated[ReadingStatusOrderSchema, Depends()],
) -> list[BookReadSchema]:
    stmt = select(Book).join(ReadingStatus).where(ReadingStatus.user_id == current_user.id)
    stmt = apply_ordering(stmt, order, ORDER_COLUMN_MAP)

    if filters.status:
        stmt = stmt.where(ReadingStatus.status == filters.status)

    result = await session.execute(stmt)
    books = result.scalars().all()

    return [BookReadSchema.model_validate(book) for book in books]
