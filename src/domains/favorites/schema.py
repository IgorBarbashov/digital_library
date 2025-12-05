import uuid
from pydantic import ConfigDict
from src.domains.common.schema import BaseSchema


class FavoriteBaseSchema(BaseSchema):
    user_id: uuid.UUID
    book_id: uuid.UUID


class FavoriteCreateSchema(FavoriteBaseSchema):

    model_config = ConfigDict(from_attributes=True)


class FavoriteUpdateSchema(FavoriteBaseSchema):

    model_config = ConfigDict(from_attributes=True)
