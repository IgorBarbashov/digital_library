from __future__ import annotations

from sqlmodel import SQLModel

from src.models.association.author_genre import AuthorGenre
from src.models.author import AuthorORM
from src.models.genre import GenreORM

__all__ = ["SQLModel", "AuthorORM", "GenreORM", "AuthorGenre"]
