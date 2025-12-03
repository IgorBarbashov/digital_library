from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schema import TokenDataSchema
from src.db.db import get_async_session
from src.domains.user.repository import get_user_orm_by_username
from src.domains.user.schema import UserReadSchema
from src.exceptions.auth import BadCredentials
from src.setting import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_base_prefix}{settings.auth_prefix}{settings.get_token_slug}"
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> UserReadSchema:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
        username = payload.get("username")

        if username is None:
            raise BadCredentials()

        token_data = TokenDataSchema(username=username)
        user = await get_user_orm_by_username(session, username=token_data.username)

        if user is None:
            raise BadCredentials()

        return UserReadSchema.from_orm(user)

    except jwt.InvalidTokenError:
        raise BadCredentials()
