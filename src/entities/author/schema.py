from datetime import date
from typing import List, Optional

from pydantic import ConfigDict

from src.entities.common.schema import BaseSchema
from src.entities.genre.schema import GenreSchema


class AuthorSchema(BaseSchema):
    first_name: str
    last_name: str
    birth_date: Optional[date]

    model_config = ConfigDict(from_attributes=True)


class AuthorWithGenreSchema(AuthorSchema):
    genres: List[GenreSchema] = []

    model_config = ConfigDict(from_attributes=True)
