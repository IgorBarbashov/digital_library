import uuid
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import SecretStr

# from src.api.v1.init import api_base_prefix
from src.constants.user_role import UserRole
from src.domains.user.schema import (
    UserReadSchema,
    UserWithPasswordReadSchema,
)

router = APIRouter()

fake_users_db: Dict[str, UserWithPasswordReadSchema] = {
    "fake_user": UserWithPasswordReadSchema(
        id=uuid.uuid4(),
        username="fake_user",
        first_name="John",
        last_name="Doe",
        email="john@fake.com",
        disabled=False,
        hashed_password=SecretStr("fakehashed_123"),
        role=UserRole("user"),
    )
}


def fake_generate_token(username: str):
    return f"{username}-{username}-{username}"


def fake_hash_password(password: str):
    return "fakehashed_" + password


# надо использовать api_base_prefix
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_user_with_password_orm_from_db(db, username: str) -> UserWithPasswordReadSchema:
    if username in db:
        return db[username]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_orm_from_db(db, username: str) -> UserReadSchema:
    user_with_password = get_user_with_password_orm_from_db(db, username)
    return UserReadSchema.model_validate({**user_with_password.model_dump()})


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserReadSchema:
    # здесь должны проводиться операции проверки токена
    # ...
    # потом из токена мы получаем username
    username = token.split("-")[0]
    # и если все ok - потом по username получаем самого user
    user = get_user_orm_from_db(fake_users_db, username)
    return user


async def get_current_active_user(
    current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> UserReadSchema:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_with_password_orm_from_db(fake_users_db, form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # нужна функция хэширования пароля
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password.get_secret_value():
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # нужна функция генерации токена
    token = fake_generate_token(user.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
):
    return current_user
