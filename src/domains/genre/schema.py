import uuid

from pydantic import ConfigDict
from src.domains.common.schema import BasePatchSchema, BaseSchema


class GenreBaseSchema(BaseSchema):
    name: str


class GenreCreateSchema(GenreBaseSchema):
    pass


class GenrePatchSchema(BasePatchSchema):
    name: str | None = None


class GenreReadSchema(BaseSchema):
    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
