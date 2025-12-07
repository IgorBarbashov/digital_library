from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.author.models import Author
    from src.domains.genre.models import Genre


class AuthorBook(Base, BaseModelMixin):
    __tablename__ = "author_book"

    author_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("author.id"), primary_key=True
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("book.id"), primary_key=True
    )

    author: Mapped[Author] = relationship(
        "Author", back_populates="author_books"
    )
    book: Mapped[Genre] = relationship(
        "Book", back_populates="author_books"
    )
