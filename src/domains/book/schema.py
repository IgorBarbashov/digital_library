import uuid
from pydantic import ConfigDict
from src.domains.common.schema import BaseSchema


class BookBaseSchema(BaseSchema):
    title: str
    genre_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BookCreateSchema(BookBaseSchema):
    model_config = ConfigDict(from_attributes=True)
