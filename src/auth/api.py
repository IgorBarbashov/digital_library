import uuid
from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import SecretStr

# from src.api.v1.init import api_base_prefix
from src.domains.user.schema import UserBaseSchema, UserWithPasswordReadSchema

router = APIRouter()

fake_users_db = {
    "fake_user": UserWithPasswordReadSchema(
        id=uuid.uuid4(),
        username="fake_user",
        first_name="John",
        last_name="Doe",
        email="john@fake.com",
        disabled=False,
        hashed_password=SecretStr("fakehashed_123"),
    )
}


def fake_generate_token(username: str):
    return f"{username}-{username}-{username}"


def fake_hash_password(password: str):
    return "fakehashed_" + password


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)  # надо использовать api_base_prefix


def get_user_orm_from_db(db, username: str):
    if username in db:
        return cast(UserWithPasswordReadSchema, db[username])


def get_user(token) -> UserBaseSchema | None:
    # здесь должны проводиться операции проверки токена
    # и если все ok - потом получение user
    user = get_user_orm_from_db(fake_users_db, token)
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserBaseSchema:
    user = get_user(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[UserBaseSchema, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = get_user_orm_from_db(fake_users_db, form_data.username)

        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        # нужна функция хэширования пароля
        hashed_password = fake_hash_password(form_data.password)

        if not hashed_password == user.hashed_password.get_secret_value():
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        # нужна функция генерации токена
        token = fake_generate_token(user.username)

        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except Exception as err:
        import traceback

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", err)
        traceback.print_exc()
        raise


@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserBaseSchema, Depends(get_current_active_user)],
):
    return current_user
