from __future__ import annotations

import uuid

from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.genre.models import Author, Genre
    from src.domains.common.association.author_book import AuthorBook


class Book(Base, BaseModelMixin):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    genre_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("genre.id"), nullable=False, unique=False
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    author_books: Mapped[List[AuthorBook]] = relationship(
        "AuthorBook", back_populates="author"
    )
