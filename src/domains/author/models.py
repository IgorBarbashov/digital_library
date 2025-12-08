from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domains.book.models import Book
from src.domains.common.association.author_book import AuthorBook
from src.domains.common.association.author_genre import AuthorGenre
from src.domains.common.association.author_book import AuthorBook
from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.genre.models import Genre
    from src.domains.book.models import Book


class Author(Base, BaseModelMixin):
    __tablename__ = "author"

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(DateTime, nullable=True, default=None)
    author_genres: Mapped[list[AuthorGenre]] = relationship(
        "AuthorGenre", back_populates="author", cascade="all, delete-orphan"
    )
    genres: Mapped[list[Genre]] = relationship(
        "Genre",
        secondary="author_genre",
        back_populates="authors",
        viewonly=True,
        lazy="select",
    )

    author_books: Mapped[list[AuthorBook]] = relationship(
        "AuthorBook", back_populates="author", cascade="all, delete-orphan", overlaps="authors,books"
    )

    books: Mapped[list[Book]] = relationship(
        "Book",
        secondary="author_book",
        back_populates="authors",
        lazy="select",
        overlaps="author,author_books,book",
    )
