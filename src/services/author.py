import uuid
from typing import List, Union

from fastapi import Depends

from src.exceptions.entity import AuthorNotFound
from src.repositories.author import AuthorRepository, get_author_repository
from src.schemas.author import AuthorResponse, AuthorWithGenreResponse


class AuthorService:
    def __init__(self, repo):
        self.repo = repo

    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> Union[List[AuthorResponse], List[AuthorWithGenreResponse]]:
        if with_genre:
            authors = await self.repo.get_all_with_genre(skip=skip, limit=limit)
            return [AuthorWithGenreResponse.from_orm(author) for author in authors]
        else:
            authors = await self.repo.get_all(skip=skip, limit=limit)
            return [AuthorResponse.from_orm(author) for author in authors]

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Union[AuthorResponse, AuthorWithGenreResponse]:
        if with_genre:
            author = await self.repo.get_by_id_with_genre(author_id)
            if not author:
                raise AuthorNotFound(author_id)
            return AuthorWithGenreResponse.from_orm(author)
        else:
            author = await self.repo.get_by_id(author_id)
            if not author:
                raise AuthorNotFound(author_id)
            return AuthorResponse.from_orm(author)


async def get_author_service(
    repo: AuthorRepository = Depends(get_author_repository),
) -> AuthorService:
    return AuthorService(repo)
