import uuid

from pydantic import ConfigDict

from src.domains.common.schema import BaseSchema


class BookBaseSchema(BaseSchema):
    title: str
    genre_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BookCreateSchema(BookBaseSchema):
    authors: list[uuid.UUID]
    model_config = ConfigDict(from_attributes=True)


class BookUpdateSchema(BaseSchema):
    title: str | None = None
    genre_id: uuid.UUID | None = None
    authors: list[uuid.UUID] | None = None


class BookReadSchema(BookBaseSchema):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BookFilters(BaseSchema):
    title: str | None = None
    genre_id: uuid.UUID | None = None
    author_id: uuid.UUID | None = None
    limit: int = 50
    offset: int = 0
