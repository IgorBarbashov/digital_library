import uuid
from pydantic import ConfigDict
from src.domains.common.schema import BaseSchema


class FavoriteBase(BaseSchema):
    user_id: uuid.UUID
    book_id: uuid.UUID


class FavoriteCreate(FavoriteBase):

    model_config = ConfigDict(from_attributes=True)


class FavoriteUpdate(FavoriteBase):

    model_config = ConfigDict(from_attributes=True)
