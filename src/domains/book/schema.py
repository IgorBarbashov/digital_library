import uuid
from src.domains.common.schema import BaseSchema


class BookBase(BaseSchema):
    title: str
    genre_id: uuid.UUID


class BookCreate(BookBase):
    pass
