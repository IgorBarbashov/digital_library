from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domains.common.association.author_genre import AuthorGenre
from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.author.models import Author


class Genre(Base, BaseModelMixin):
    __tablename__ = "genre"

    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    author_genres: Mapped[list[AuthorGenre]] = relationship(
        "AuthorGenre", back_populates="genre", cascade="all, delete-orphan"
    )
    authors: Mapped[list[Author]] = relationship(
        "Author",
        secondary="author_genre",
        back_populates="genres",
        viewonly=True,
        lazy="select",
    )
