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


class AuthorGenre(Base, BaseModelMixin):
    __tablename__ = "author_genre"

    author_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("author.id"), primary_key=True
    )
    genre_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("genre.id"), primary_key=True
    )

    author: Mapped["Author"] = relationship("Author", back_populates="author_genres")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="author_genres")
