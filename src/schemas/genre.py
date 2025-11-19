from pydantic import ConfigDict

from src.schemas.base import BaseSchema


class GenreSchema(BaseSchema):
    name: str

    model_config = ConfigDict(from_attributes=True)
