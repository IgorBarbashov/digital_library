from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.author.models import Author
    from src.domains.genre.models import Genre


class AuthorGenre(Base, BaseModelMixin):
    __tablename__ = "author_genre"

    __table_args__ = (
        UniqueConstraint("author_id", "genre_id", name="uc_author_genre"),
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("author.id", ondelete="CASCADE"),
        nullable=False,
    )
    genre_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("genre.id", ondelete="CASCADE"),
        nullable=False,
    )

    author: Mapped[Author] = relationship("Author", back_populates="author_genres")
    genre: Mapped[Genre] = relationship("Genre", back_populates="author_genres")
