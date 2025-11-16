from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.association.author_genre import AuthorGenre
from src.models.base import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.models.genre import Genre


class Author(Base, BaseModelMixin):
    __tablename__ = "author"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[Optional[date]] = mapped_column(
        DateTime, nullable=True, default=None
    )
    author_genres: Mapped[List[AuthorGenre]] = relationship(
        "AuthorGenre", back_populates="author"
    )
    genres: Mapped[List["Genre"]] = relationship(
        "Genre",
        secondary="author_genre",
        back_populates="authors",
        viewonly=True,
        lazy="select",
    )
