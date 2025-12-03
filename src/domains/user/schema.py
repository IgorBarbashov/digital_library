from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from pydantic import AliasPath, ConfigDict, EmailStr, Field, SecretStr

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
    password: SecretStr = Field(validation_alias=AliasPath("hashed_password"))
    role: UserRole

    model_config = ConfigDict(
        alias_generator=lambda x: x.replace("password", "hashed_password"),
        populate_by_name=True,
    )

    def to_orm_dict(self) -> Dict[str, Any]:
        data = self.model_dump(by_alias=True, exclude={"role"})
        password = data.get("hashed_password")

        if isinstance(password, SecretStr):
            data["hashed_password"] = password.get_secret_value()

        return data


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
