import uuid
from datetime import datetime

from pydantic import ConfigDict, Field

from src.domains.common.schema import BaseSchema


class CategoryBaseSchema(BaseSchema):

    name: str = Field(
        ..., min_length=1, max_length=100, description="Название категории"
    )


class CategoryCreateSchema(CategoryBaseSchema):

    pass


class CategoryPatchSchema(BaseSchema):

    name: str | None = Field(
        None, min_length=1, max_length=100, description="Название категории"
    )


class CategoryReadSchema(CategoryBaseSchema):

    id: uuid.UUID
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)
