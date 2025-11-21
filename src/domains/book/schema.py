import uuid
from src.domains.common.schema import BaseSchema


class BookBase(BaseSchema):
    title: str
    author_id: uuid.UUID
    genre_id: uuid.UUID


class BookCreate(BookBase):
    pass
