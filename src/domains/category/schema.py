import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryBaseSchema(BaseModel):
    """Base category schema."""

    name: str = Field(
        ..., min_length=1, max_length=100, description="Название категории"
    )


class CategoryCreateSchema(CategoryBaseSchema):
    """Schema for creating a category."""

    pass


class CategoryPatchSchema(BaseModel):
    """Schema for updating a category."""

    name: str | None = Field(
        None, min_length=1, max_length=100, description="Название категории"
    )


class CategoryReadSchema(CategoryBaseSchema):
    """Schema for reading a category."""

    id: uuid.UUID
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)
