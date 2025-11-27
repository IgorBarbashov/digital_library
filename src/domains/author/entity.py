import uuid
from datetime import date
from typing import List, Optional


class AuthorEntity:
    first_name: str
    last_name: str
    genres: List[uuid.UUID]
    id: Optional[uuid.UUID]
    birth_date: Optional[date]

    def __init__(
        self,
        first_name: str,
        last_name: str,
        genres: List[uuid.UUID],
        id: Optional[uuid.UUID] = None,
        birth_date: Optional[date] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.genres = genres
        self.id = id
        self.birth_date = birth_date
