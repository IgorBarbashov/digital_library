import uuid
from typing import Optional

from pydantic import ConfigDict

from src.domains.common.schema import BaseSchema


class GenreBaseSchema(BaseSchema):
    name: str


class GenreCreateSchema(GenreBaseSchema):
    pass


class GenreUpdateSchema(BaseSchema):
    name: Optional[str] = None


class GenreReadSchema(BaseSchema):
    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
