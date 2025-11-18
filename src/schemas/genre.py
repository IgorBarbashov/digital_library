from pydantic import ConfigDict

from src.schemas.base import BaseEntity, BaseEntityResponse


class GenreBase(BaseEntity):
    name: str


class GenreResponse(GenreBase, BaseEntityResponse):
    model_config = ConfigDict(from_attributes=True)
