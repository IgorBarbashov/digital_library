from pydantic import BaseModel


class TokenReadSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str
