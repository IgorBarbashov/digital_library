from __future__ import annotations

import uuid
from typing import Any

from pydantic import ConfigDict, EmailStr, SecretStr

from src.constants.pagination import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET
from src.constants.user_role import UserRole
from src.domains.common.schema import BasePatchSchema, BaseSchema, OrderBaseSchema
from src.domains.user.constants import UserOrderBy
from src.domains.user.models import User


class UserBaseSchema(BaseSchema):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    disabled: bool


class UserCreateSchema(UserBaseSchema):
    password: SecretStr
    role: UserRole

    def to_orm_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude={"role", "password"})


class UserPatchSchema(BasePatchSchema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    disabled: bool | None = None


class UserUpdateSchema(UserBaseSchema):
    pass


class UserReadSchema(UserBaseSchema):
    id: uuid.UUID
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj: User) -> UserReadSchema:
        return cls.model_validate(
            {
                **obj.__dict__,
                "role": UserRole(obj.role.name),
            }
        )


class UserWithPasswordReadSchema(UserReadSchema):
    hashed_password: SecretStr


class AssignUserRoleSchema(BaseSchema):
    role: UserRole


class UserFiltersSchema(BaseSchema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    limit: int = DEFAULT_PAGINATION_LIMIT
    offset: int = DEFAULT_PAGINATION_OFFSET


class UserOrderSchema(OrderBaseSchema):
    order_by: UserOrderBy = UserOrderBy.create_at
