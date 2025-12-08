import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domains.book.models import Book
from src.domains.common.models import Base, CreatedUpdatedColumnsMixin

if TYPE_CHECKING:
    from src.domains.author.models import Author


class AuthorBook(Base, CreatedUpdatedColumnsMixin):
    __tablename__ = "author_book"

    author_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "author.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "book.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    author: Mapped[Author] = relationship("Author", back_populates="author_books", overlaps="authors,books")
    book: Mapped[Book] = relationship("Book", back_populates="author_books", overlaps="authors,books")
