from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.author.models import Author
    from src.domains.book.models import Book


class AuthorBook(Base, BaseModelMixin):
    __tablename__ = "author_book"

    __table_args__ = (
        UniqueConstraint("author_id", "book_id", name="uc_author_book"),
    )

    author_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("author.id"), primary_key=True)
    book_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("book.id"), primary_key=True)

    author: Mapped["Author"] = relationship("Author", back_populates="author_books")
    book: Mapped["Book"] = relationship("Book", back_populates="author_books")
