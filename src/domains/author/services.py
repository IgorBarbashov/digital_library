import uuid
from typing import List, Union

from fastapi import Depends

from src.domains.author.protocols import AuthorRepository
from src.domains.author.repository import get_author_repository
from src.domains.author.schema import AuthorSchema, AuthorWithGenreSchema
from src.exceptions.entity import EntityNotFound


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
            raise EntityNotFound({"id": author_id}, entity_name="author")

        return author


async def get_author_service(
    repo: AuthorRepository = Depends(get_author_repository),
) -> AuthorService:
    return AuthorService(repo)
