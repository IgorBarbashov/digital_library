import uuid
from pydantic import ConfigDict
from src.domains.common.schema import BaseSchema


class BookBase(BaseSchema):
    title: str
    genre_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    model_config = ConfigDict(from_attributes=True)
