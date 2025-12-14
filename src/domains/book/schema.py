import uuid
from typing import Self

from pydantic import ConfigDict

from src.constants.reading_status import BookReadingStatus
from src.domains.book.models import Book
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


class BookWithReadingStatusReadSchema(BookReadSchema):
    status: BookReadingStatus

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_status(cls, book: Book, status: BookReadingStatus) -> Self:
        base = BookReadSchema.model_validate(book).model_dump()
        data = {**base, "status": status}
        return cls.model_validate(data)


class BookFilters(BaseSchema):
    title: str | None = None
    genre_id: uuid.UUID | None = None
    author_id: uuid.UUID | None = None
    limit: int = 50
    offset: int = 0


class BookInformationSchema(BaseSchema):
    id: uuid.UUID
    title: str
    authors: list
    description: str | None
    genre_id: uuid.UUID
    category_id: uuid.UUID | None
    average_rating: float | None
    total_ratings: int
    max_rating_count: int
    text_reviews_count: int
    latest_reviews: list

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
