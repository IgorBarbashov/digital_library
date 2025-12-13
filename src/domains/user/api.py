import uuid
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy import delete, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.guards import get_current_active_user
from src.auth.utils import get_password_hash
from src.db.db import get_async_session
from src.domains.role.repository import get_role_orm_by_name
from src.domains.user.constants import ORDER_COLUMN_MAP
from src.domains.user.models import User
from src.domains.user.repository import get_user_orm_by_id
from src.domains.user.schema import (
    AssignUserRoleSchema,
    UserCreateSchema,
    UserFiltersSchema,
    UserOrderSchema,
    UserPatchSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from src.exceptions.entity import EntityAlreadyExists, EntityNotFound
from src.utils.request_builder import apply_ordering

router = APIRouter()


@router.get(
    "/",
    summary="Получить список пользователей",
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    filters: Annotated[UserFiltersSchema, Depends()],
    order: Annotated[UserOrderSchema, Depends()],
) -> list[UserReadSchema]:
    stmt = select(User).options(selectinload(User.role))
    stmt = stmt.limit(filters.limit).offset(filters.offset)
    stmt = apply_ordering(stmt, order, ORDER_COLUMN_MAP)

    if filters.username:
        stmt = stmt.where(User.username.ilike(f"%{filters.username}%"))

    if filters.first_name:
        stmt = stmt.where(User.first_name.ilike(f"%{filters.first_name}%"))

    if filters.last_name:
        stmt = stmt.where(User.last_name.ilike(f"%{filters.last_name}%"))

    if filters.email:
        stmt = stmt.where(User.email.ilike(f"%{filters.email}%"))

    result = await session.execute(stmt)
    users = result.scalars().all()

    return [UserReadSchema.from_orm(user) for user in users]


@router.get(
    "/me",
    summary="Получить информацию по текущему пользователю",
)
async def get_me(
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
) -> UserReadSchema:
    return current_user


@router.get(
    "/{user_id}",
    summary="Получить пользователя по id",
)
async def get_by_id(
    user_id: Annotated[uuid.UUID, Path(..., description="ID пользователя")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserReadSchema:
    user = await get_user_orm_by_id(session, user_id)
    return UserReadSchema.from_orm(user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя",
)
async def create_user(
    user_data: UserCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserReadSchema:
    try:
        role = await get_role_orm_by_name(session, user_data.role)
        hashed_password = get_password_hash(user_data.password.get_secret_value())
        user = User(
            **user_data.to_orm_dict(),
            role=role,
            hashed_password=hashed_password,
        )

        session.add(user)
        await session.commit()

        return UserReadSchema.from_orm(user)

    except IntegrityError:
        raise EntityAlreadyExists(
            {"username": user_data.username, "email": user_data.email},
            entity_name="user",
        ) from None


@router.patch(
    "/{user_id}",
    summary="Частичное обновление пользователя",
)
async def patch_user(
    user_data: UserPatchSchema,
    user_id: Annotated[uuid.UUID, Path(..., description="ID пользователя")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserReadSchema:
    update_data = user_data.model_dump(exclude_unset=True)
    stmt = update(User).where(User.id == user_id).values(**update_data)
    result = await session.execute(stmt)
    cursor_result = cast(CursorResult, result)

    if cursor_result.rowcount == 0:
        raise EntityNotFound({"id": user_id}, entity_name="user")

    await session.commit()
    user = await get_user_orm_by_id(session, user_id)

    return UserReadSchema.from_orm(user)


@router.put(
    "/{user_id}",
    summary="Полное обновление пользователя",
)
async def update_user(
    user_data: UserUpdateSchema,
    user_id: Annotated[uuid.UUID, Path(..., description="ID пользователя")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserReadSchema:
    update_user = UserPatchSchema(**user_data.model_dump())
    return await patch_user(user_data=update_user, user_id=user_id, session=session)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя по id",
)
async def delete_user(
    user_id: Annotated[uuid.UUID, Path(..., description="ID пользователя")],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    stmt = delete(User).where(User.id == user_id).returning(User.id)
    result = await session.execute(stmt)
    deleted_ids = [row[0] for row in result]

    if not deleted_ids:
        raise EntityNotFound({"id": user_id}, entity_name="user")

    await session.commit()


@router.post(
    "/{user_id}/assign-role",
    status_code=status.HTTP_200_OK,
    summary="Назначить роль пользователю",
)
async def assign_role_to_user(
    user_id: uuid.UUID,
    user_data: AssignUserRoleSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    role_id = (await get_role_orm_by_name(session, user_data.role)).id
    user = await get_user_orm_by_id(session, user_id)

    user.role_id = role_id
    session.add(user)
    await session.commit()
