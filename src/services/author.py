import uuid
from typing import List, Union

from fastapi import Depends

from src.exceptions.entity import AuthorNotFound
from src.repositories.author import AuthorRepository, get_author_repository
from src.schemas.author import Author, AuthorWithGenre


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> Union[List[Author], List[AuthorWithGenre]]:
        return await self.repo.get_all(skip=skip, limit=limit, with_genre=with_genre)

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Union[Author, AuthorWithGenre]:
        author = await self.repo.get_by_id(author_id=author_id, with_genre=with_genre)

        if author is None:
            raise AuthorNotFound(author_id)

        return author


async def get_author_service(
    repo: AuthorRepository = Depends(get_author_repository),
) -> AuthorService:
    return AuthorService(repo)
