from src.domains.common.schema import BaseSchema


class UserBase(BaseSchema):
    username: str
    email: str


class UserCreate(UserBase):
    pass
