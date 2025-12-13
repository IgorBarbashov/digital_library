import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.guards import get_current_user
from src.db.db import get_async_session
from src.domains.review.models import Review
from src.domains.review.schema import (
    ReviewCreateSchema,
    ReviewPatchSchema,
    ReviewReadSchema,
)
from src.domains.user.models import User
from src.exceptions.entity import EntityNotFound

router = APIRouter()


@router.get(
    "/",
    summary="Получить список всех отзывов",
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    book_id: uuid.UUID | None = None,
) -> list[ReviewReadSchema]:
    stmt = select(Review).order_by(Review.create_at.desc())

    if book_id:
        stmt = stmt.where(Review.book_id == book_id)

    result = await session.execute(stmt)
    reviews = result.scalars().all()

    return [ReviewReadSchema.model_validate(review) for review in reviews]


@router.get(
    "/{review_id}",
    summary="Получить отзыв по id",
)
async def get_by_id(
    review_id: Annotated[uuid.UUID, Path(..., description="ID отзыва")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ReviewReadSchema:
    review = await session.get(Review, review_id)

    if review is None:
        raise EntityNotFound({"id": review_id}, entity_name="review")

    return ReviewReadSchema.model_validate(review)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать отзыв",
)
async def create(
    review_in: ReviewCreateSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ReviewReadSchema:
    review = Review(
        user_id=current_user.id,
        **review_in.model_dump(),
    )

    session.add(review)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise EntityNotFound(
            {"book_id": review_in.book_id}, entity_name="book"
        ) from None

    await session.refresh(review)

    return ReviewReadSchema.model_validate(review)


@router.patch(
    "/{review_id}",
    summary="Обновить отзыв",
)
async def patch(
    review_id: Annotated[uuid.UUID, Path(..., description="ID отзыва")],
    review_in: ReviewPatchSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ReviewReadSchema:
    review = await session.get(Review, review_id)

    if review is None:
        raise EntityNotFound({"id": review_id}, entity_name="review")

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only update your own reviews"
        )

    stmt = (
        update(Review)
        .where(Review.id == review_id)
        .values(**review_in.model_dump(exclude_unset=True))
    )

    await session.execute(stmt)
    await session.commit()
    await session.refresh(review)

    return ReviewReadSchema.model_validate(review)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить отзыв",
)
async def delete_by_id(
    review_id: Annotated[uuid.UUID, Path(..., description="ID отзыва")],
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    review = await session.get(Review, review_id)

    if review is None:
        raise EntityNotFound({"id": review_id}, entity_name="review")

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only delete your own reviews"
        )

    stmt = delete(Review).where(Review.id == review_id)
    await session.execute(stmt)
    await session.commit()
