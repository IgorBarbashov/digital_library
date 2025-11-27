import uuid
from typing import List, Optional, Protocol

from src.domains.author.entity import AuthorEntity
from src.domains.author.models import Author


class AuthorRepository(Protocol):
    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> List[AuthorEntity]: ...

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Optional[AuthorEntity]: ...

    async def create(self, author: AuthorEntity) -> AuthorEntity: ...

    async def delete(self, author_id: uuid.UUID) -> bool: ...

    async def get_by_id_orm(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Optional[Author]: ...
