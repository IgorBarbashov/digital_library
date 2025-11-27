import uuid
from datetime import date
from typing import List, Optional, Sequence

from pydantic import ConfigDict

from src.domains.author.entity import AuthorEntity
from src.domains.author.models import Author
from src.domains.common.schema import BaseSchema


class AuthorBaseSchema(BaseSchema):
    first_name: str
    last_name: str
    genres: List[uuid.UUID]
    birth_date: Optional[date] = None


class AuthorReadSchema(AuthorBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorUpdateSchema(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    genres: Optional[List[uuid.UUID]] = None
    birth_date: Optional[date] = None


class AuthorResponseSchema(AuthorBaseSchema):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class AuthorMappers:
    @staticmethod
    def dto_to_entity_create(author_create: AuthorCreateSchema) -> AuthorEntity:
        return AuthorEntity(
            first_name=author_create.first_name,
            last_name=author_create.last_name,
            birth_date=author_create.birth_date,
            genres=author_create.genres,
        )

    @staticmethod
    def entity_to_orm(author: AuthorEntity) -> Author:
        return Author(
            first_name=author.first_name,
            last_name=author.last_name,
            birth_date=author.birth_date,
        )

    @staticmethod
    def orm_to_entity(author_orm: Author, with_genre: bool = False) -> AuthorEntity:
        return AuthorEntity(
            first_name=author_orm.first_name,
            last_name=author_orm.last_name,
            genres=AuthorMappers.get_author_genre_ids(author_orm, with_genre),
            id=author_orm.id,
            birth_date=author_orm.birth_date,
        )

    @staticmethod
    def orm_to_entity_list(
        authors_orm: Sequence[Author], with_genre: bool = False
    ) -> List[AuthorEntity]:
        return [
            AuthorMappers.orm_to_entity(author_orm, with_genre)
            for author_orm in authors_orm
        ]

    @staticmethod
    def entity_to_response(author: AuthorEntity) -> AuthorResponseSchema:
        return AuthorResponseSchema.model_validate(author)

    @staticmethod
    def entity_to_response_list(
        authors: List[AuthorEntity],
    ) -> List[AuthorResponseSchema]:
        return [AuthorMappers.entity_to_response(author) for author in authors]

    @staticmethod
    def get_author_genre_ids(
        author_orm: Author, with_genre: bool = False
    ) -> List[uuid.UUID]:
        if not with_genre:
            return []

        genres = getattr(author_orm, "genres", None)
        return [genre.id for genre in genres] if genres else []
