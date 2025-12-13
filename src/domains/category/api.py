import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.guards import get_current_active_admin
from src.db.db import get_async_session
from src.domains.category.models import Category
from src.domains.category.schema import (
    CategoryCreateSchema,
    CategoryPatchSchema,
    CategoryReadSchema,
)
from src.domains.user.schema import UserReadSchema
from src.exceptions.entity import EntityAlreadyExists, EntityNotFound

router = APIRouter()


@router.get(
    "/",
    summary="Получить список категорий",
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[CategoryReadSchema]:
    stmt = select(Category).order_by(Category.create_at.asc())
    result = await session.execute(stmt)
    categories = result.scalars().all()

    return [CategoryReadSchema.model_validate(category) for category in categories]


@router.get(
    "/{category_id}",
    summary="Получить категорию по id",
)
async def get_by_id(
    category_id: Annotated[uuid.UUID, Path(..., description="ID категории")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> CategoryReadSchema:
    category = await session.get(Category, category_id)

    if category is None:
        raise EntityNotFound({"id": category_id}, entity_name="category")

    return CategoryReadSchema.model_validate(category)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию",
)
async def create(
    category_in: CategoryCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_admin: Annotated[UserReadSchema, Depends(get_current_active_admin)],
) -> CategoryReadSchema:
    category = Category(**category_in.model_dump())

    session.add(category)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise EntityAlreadyExists(
            {"name": category_in.name}, entity_name="category"
        ) from None

    return CategoryReadSchema.model_validate(category)


@router.patch(
    "/{category_id}",
    summary="Обновить категорию",
)
async def patch(
    category_id: Annotated[uuid.UUID, Path(..., description="ID категории")],
    category_in: CategoryPatchSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_admin: Annotated[UserReadSchema, Depends(get_current_active_admin)],
) -> CategoryReadSchema:
    category = await session.get(Category, category_id)

    if category is None:
        raise EntityNotFound({"id": category_id}, entity_name="category")

    stmt = (
        update(Category)
        .where(Category.id == category_id)
        .values(**category_in.model_dump(exclude_unset=True))
    )

    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise EntityAlreadyExists(
            category_in.model_dump(exclude_unset=True), entity_name="category"
        ) from None

    await session.refresh(category)

    return CategoryReadSchema.model_validate(category)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_by_id(
    category_id: Annotated[uuid.UUID, Path(..., description="ID категории")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_admin: Annotated[UserReadSchema, Depends(get_current_active_admin)],
) -> None:
    category = await session.get(Category, category_id)

    if category is None:
        raise EntityNotFound({"id": category_id}, entity_name="category")

    stmt = delete(Category).where(Category.id == category_id)
    await session.execute(stmt)
    await session.commit()
