from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.association.author_genre import AuthorGenre
from src.models.base import Base, BaseModelMixin


class Genre(Base, BaseModelMixin):
    __tablename__ = "genre"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    author_genres: Mapped[List[AuthorGenre]] = relationship(
        "AuthorGenre", back_populates="genre"
    )
    authors: Mapped[List["Author"]] = relationship(
        "Author",
        secondary="author_genre",
        back_populates="genres",
        viewonly=True,
        lazy="select",
    )
