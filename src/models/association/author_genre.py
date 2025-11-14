from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel  # type: ignore


class AuthorGenre(SQLModel, table=True):
    __tablename__ = "author_genre"  # type: ignore

    author_id: Optional[int] = Field(
        default=None, foreign_key="author.id", primary_key=True
    )
    genre_id: Optional[int] = Field(
        default=None, foreign_key="genre.id", primary_key=True
    )
