import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domains.common.association.author_book import AuthorBook
from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.author.models import Author
    from src.domains.common.association.author_book import AuthorBook
    from src.domains.favorites.models import Favorites
    from src.domains.genre.models import Genre


class Book(Base, BaseModelMixin):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    genre_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("genre.id"), nullable=False, unique=False
    )
    genre: Mapped["Genre"] = relationship("Genre", back_populates="book")

    favorites: Mapped[list[Favorites]] = relationship("Favorites", back_populates="book", cascade="all, delete-orphan")

    author_books: Mapped[list[AuthorBook]] = relationship(
        "AuthorBook", back_populates="book", cascade="all, delete-orphan", overlaps="authors"
    )

    authors: Mapped[list[Author]] = relationship(
        "Author",
        secondary="author_book",
        back_populates="books",
        lazy="select",
        overlaps="author_books",
    )
