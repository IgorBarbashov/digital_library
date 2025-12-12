from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.user.repository import get_user_orm_by_username
from src.domains.user.schema import UserReadSchema
from src.exceptions.auth import IncorrectUsernamePassword
from src.exceptions.entity import EntityNotFound
from src.setting import settings

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> UserReadSchema:
    try:
        user = await get_user_orm_by_username(session, username)

        if not verify_password(password, user.hashed_password):
            raise IncorrectUsernamePassword()

        return UserReadSchema.from_orm(user)

    except EntityNotFound:
        raise IncorrectUsernamePassword() from None


def create_access_token(user: UserReadSchema) -> str:
    now = datetime.now(timezone.utc)
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = now + expires_delta
    to_encode = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role.value,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )

    return encoded_jwt
