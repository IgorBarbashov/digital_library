from pydantic import ConfigDict

from src.domains.common.schema import BaseSchema


class GenreSchema(BaseSchema):
    name: str

    model_config = ConfigDict(from_attributes=True)
