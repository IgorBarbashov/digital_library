from datetime import date
from typing import List, Optional

from pydantic import ConfigDict

from src.schemas.base import BaseSchema
from src.schemas.genre import GenreSchema


class AuthorSchema(BaseSchema):
    first_name: str
    last_name: str
    birth_date: Optional[date]

    model_config = ConfigDict(from_attributes=True)


class AuthorWithGenreSchema(AuthorSchema):
    genres: List[GenreSchema] = []

    model_config = ConfigDict(from_attributes=True)
