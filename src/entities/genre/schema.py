from pydantic import ConfigDict

from src.entities.common.schema import BaseSchema


class GenreSchema(BaseSchema):
    name: str

    model_config = ConfigDict(from_attributes=True)
