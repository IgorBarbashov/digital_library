from pydantic import ConfigDict

from src.schemas.base import BaseEntity


class Genre(BaseEntity):
    name: str

    model_config = ConfigDict(from_attributes=True)
