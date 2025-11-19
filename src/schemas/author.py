from datetime import date
from typing import List, Optional

from pydantic import ConfigDict

from src.schemas.base import BaseEntity
from src.schemas.genre import Genre


class Author(BaseEntity):
    first_name: str
    last_name: str
    birth_date: Optional[date]

    model_config = ConfigDict(from_attributes=True)


class AuthorWithGenre(Author):
    genres: List[Genre] = []

    model_config = ConfigDict(from_attributes=True)
