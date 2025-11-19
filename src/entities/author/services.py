import uuid
from typing import List, Union

from fastapi import Depends

from src.entities.author.domain_services import AuthorRepository
from src.entities.author.repository import get_author_repository
from src.entities.author.schema import AuthorSchema, AuthorWithGenreSchema
from src.exceptions.entity import AuthorNotFound


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> Union[List[AuthorSchema], List[AuthorWithGenreSchema]]:
        return await self.repo.get_all(skip=skip, limit=limit, with_genre=with_genre)

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Union[AuthorSchema, AuthorWithGenreSchema]:
        author = await self.repo.get_by_id(author_id=author_id, with_genre=with_genre)

        if author is None:
            raise AuthorNotFound(author_id)

        return author


async def get_author_service(
    repo: AuthorRepository = Depends(get_author_repository),
) -> AuthorService:
    return AuthorService(repo)
