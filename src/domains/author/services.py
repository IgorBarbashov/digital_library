import uuid
from typing import List

from fastapi import Depends

from src.domains.author.entity import AuthorEntity
from src.domains.author.protocols import AuthorRepository
from src.domains.author.repository import get_author_repository
from src.exceptions.entity import EntityNotFound


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> List[AuthorEntity]:
        return await self.repo.get_all(skip=skip, limit=limit, with_genre=with_genre)

    async def get_by_id(self, author_id: uuid.UUID, with_genre: bool) -> AuthorEntity:
        author = await self.repo.get_by_id(author_id=author_id, with_genre=with_genre)

        if author is None:
            raise EntityNotFound({"id": author_id}, entity_name="author")

        return author

    async def create(self, author: AuthorEntity) -> AuthorEntity:
        return await self.repo.create(author)

    async def update(self, author_id: uuid.UUID, author_data: dict) -> AuthorEntity:
        update_data = {k: v for k, v in author_data.items() if v is not None}
        updated_author = await self.repo.update(author_id, update_data)

        if updated_author is None:
            raise AuthorNotFound(author_id)

        return updated_author

    async def delete(self, author_id: uuid.UUID) -> bool:
        result = await self.repo.delete(author_id)

        if not result:
            raise AuthorNotFound(author_id)

        return False


async def get_author_service(
    repo: AuthorRepository = Depends(get_author_repository),
) -> AuthorService:
    return AuthorService(repo)
