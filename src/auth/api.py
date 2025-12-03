from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.guards import get_current_active_user
from src.auth.schema import SetPasswordSchema, TokenReadSchema
from src.auth.utils import authenticate_user, create_access_token, get_password_hash
from src.db.db import get_async_session
from src.domains.user.models import User
from src.domains.user.schema import UserReadSchema
from src.setting import settings

router = APIRouter()


@router.post(
    "/token",
    response_model=TokenReadSchema,
    summary="Получить токен пользователя",
)
async def get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> TokenReadSchema:
    user = await authenticate_user(session, form_data.username, form_data.password)
    token = create_access_token(user)
    return TokenReadSchema(access_token=token, token_type=settings.access_token_type)


@router.post(
    "/set-password",
    status_code=status.HTTP_200_OK,
    summary="Установить пароль текущего пользователя",
)
async def current_user_set_password(
    user_data: SetPasswordSchema,
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> None:
    hashed_password = get_password_hash(user_data.password.get_secret_value())
    stmt = (
        update(User)
        .where(User.id == current_user.id)
        .values({"hashed_password": hashed_password})
    )
    await session.execute(stmt)
    await session.commit()
