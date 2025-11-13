from __future__ import annotations

from datetime import date
from typing import List, Optional

from association.author_genre import AuthorGenre
from genre import GenreORM
from sqlmodel import Field, Relationship, SQLModel  # type: ignore


class AuthorORM(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    birth_date: Optional[date] = Field(default=None)
    genres: List[GenreORM] = Relationship(
        back_populates="authors", link_model=AuthorGenre
    )
