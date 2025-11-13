from __future__ import annotations

from sqlmodel import SQLModel

from .association.author_genre import AuthorGenre
from .author import AuthorORM
from .genre import GenreORM

__all__ = ["SQLModel", "AuthorORM", "GenreORM", "AuthorGenre"]
