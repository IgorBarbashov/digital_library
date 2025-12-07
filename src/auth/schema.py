from pydantic import SecretStr
from src.domains.common.schema import BaseSchema


class TokenReadSchema(BaseSchema):
    access_token: str
    token_type: str


class TokenDataSchema(BaseSchema):
    username: str


class SetPasswordSchema(BaseSchema):
    password: SecretStr
