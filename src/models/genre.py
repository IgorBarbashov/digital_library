from __future__ import annotations

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from src.models.association.author_genre import AuthorGenre


class GenreORM(SQLModel, table=True):
    __tablename__ = "genre"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., unique=True)
    authors: List["AuthorORM"] = Relationship(
        back_populates="genres", link_model=AuthorGenre
    )
