import uuid
from typing import List, Optional, Protocol, Union

from src.domains.author.schema import AuthorSchema, AuthorWithGenreSchema


class AuthorRepository(Protocol):
    async def get_all(
        self, skip: int, limit: int, with_genre: bool
    ) -> Union[List[AuthorSchema], List[AuthorWithGenreSchema]]: ...

    async def get_by_id(
        self, author_id: uuid.UUID, with_genre: bool
    ) -> Union[Optional[AuthorSchema], Optional[AuthorWithGenreSchema]]: ...

    async def delete(self, author_id: uuid.UUID) -> bool: ...
