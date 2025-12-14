from enum import StrEnum

from sqlalchemy.orm import InstrumentedAttribute

from src.domains.book.models import Book


class BookOrderBy(StrEnum):
    title_ = "title"
    genre_id = "genre_id"
    author_id = "author_id"
    create_at = "create_at"


ORDER_COLUMN_MAP: dict[BookOrderBy, InstrumentedAttribute] = {
    BookOrderBy.title_: Book.title,
    BookOrderBy.genre_id: Book.genre_id,
    BookOrderBy.author_id: Book.author_books,
    BookOrderBy.create_at: Book.create_at,
}
