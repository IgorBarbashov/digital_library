import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.guards import get_current_active_user
from src.db.db import get_async_session
from src.domains.favorites.repository import (
    create_favorite,
    delete_favorite,
    get_favorite,
    list_favorites_by_user,
)
from src.domains.favorites.schema import FavoriteCreateSchema, FavoriteReadSchema
from src.domains.user.schema import UserReadSchema

router = APIRouter(prefix="", tags=["Favorites"])


@router.post(
    "/",
    response_model=FavoriteCreateSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить книгу в избранное",
)
async def add_to_favorites(
    schema: FavoriteCreateSchema,
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> FavoriteReadSchema:
    if schema.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя добавлять в избранное для другого пользователя",
        )
    
    try:
        favorite = await create_favorite(session, schema.user_id, schema.book_id)
        return FavoriteReadSchema.model_validate(favorite)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Книга уже в избранном"
        ) from e
  

@router.get(
    "/",
    summary="Получить список избранного для текущего пользователя",
)
async def get_my_favorites(
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[FavoriteReadSchema]:
    favorites = await list_favorites_by_user(session, current_user.id)
    return [FavoriteReadSchema.model_validate(f) for f in favorites]


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить книгу из избранного",
)
async def remove_from_favorites(
    book_id: uuid.UUID,
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    success = await delete_favorite(session, current_user.id, book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена в избранном",
        )
    return
