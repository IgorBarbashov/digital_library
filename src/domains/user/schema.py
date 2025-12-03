from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from pydantic import ConfigDict, EmailStr, SecretStr

from src.constants.user_role import UserRole
from src.domains.common.schema import BasePatchSchema, BaseSchema
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

    def to_orm_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude={"role", "password"})


class UserPatchSchema(BasePatchSchema):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    disabled: Optional[bool] = None


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


class SetUserPasswordSchema(BaseSchema):
    password: SecretStr
