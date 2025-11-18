from datetime import date
from typing import List, Optional

from pydantic import ConfigDict

from src.schemas.base import BaseEntity, BaseEntityResponse
from src.schemas.genre import GenreResponse


class AuthorBase(BaseEntity):
    first_name: str
    last_name: str
    birth_date: Optional[date]


class AuthorResponse(AuthorBase, BaseEntityResponse):
    model_config = ConfigDict(from_attributes=True)


class AuthorWithGenreResponse(AuthorResponse):
    genres: List[GenreResponse] = []

    model_config = ConfigDict(from_attributes=True)
