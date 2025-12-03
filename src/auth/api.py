from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schema import TokenReadSchema
from src.auth.utils import authenticate_user, create_access_token
from src.db.db import get_async_session
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
