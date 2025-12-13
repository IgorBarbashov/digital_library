import uuid
from datetime import date
from typing import Self

from pydantic import ConfigDict

from src.domains.author.models import Author
from src.domains.common.schema import BasePatchSchema, BaseSchema


class AuthorBaseSchema(BaseSchema):
    first_name: str
    last_name: str
    genres: list[uuid.UUID]
    birth_date: date | None = None


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorPatchSchema(BasePatchSchema):
    first_name: str | None = None
    last_name: str | None = None
    genres: list[uuid.UUID] | None = None
    birth_date: date | None = None


class AuthorReadSchema(AuthorBaseSchema):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_genres(cls, obj: Author, with_genre: bool) -> Self:
        genre_ids = [genre.id for genre in obj.genres] if with_genre and obj.genres else []
        author_data = {**obj.__dict__, "genres": genre_ids}

        return cls.model_validate(author_data)
