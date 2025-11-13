from __future__ import annotations

from typing import List, Optional

from association.author_genre import AuthorGenre
from author import AuthorORM
from sqlmodel import Field, Relationship, SQLModel  # type: ignore


class GenreORM(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    authors: List[AuthorORM] = Relationship(
        back_populates="genres", link_model=AuthorGenre
    )
