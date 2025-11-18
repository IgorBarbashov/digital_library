import uuid
from typing import List

from fastapi import Depends

from src.exceptions.entity import AuthorNotFound
from src.repositories.author import AuthorRepository, get_author_reposetory
from src.schemas.author import AuthorResponse


class AuthorService:
    def __init__(self, repo):
        self.repo = repo

    async def get_all(self, skip: int, limit: int) -> List[AuthorResponse]:
        authors = await self.repo.get_all(skip=skip, limit=limit)

        return authors

    async def get_by_id(self, author_id: uuid.UUID) -> AuthorResponse:
        author = await self.repo.get_by_id(author_id)

        if not author:
            raise AuthorNotFound(author_id)

        return author


async def get_author_service(
    repo: AuthorRepository = Depends(get_author_reposetory),
) -> AuthorService:
    return AuthorService(repo)
