import uuid
from datetime import datetime

from pydantic import ConfigDict, Field

from src.domains.common.schema import BaseSchema


class ReviewBaseSchema(BaseSchema):

    rating: int = Field(..., ge=1, le=5, description="Оценка книги от 1 до 5")
    text: str | None = Field(None, description="Текстовый отзыв на книгу")


class ReviewCreateSchema(ReviewBaseSchema):

    book_id: uuid.UUID = Field(..., description="ID книги")


class ReviewPatchSchema(BaseSchema):

    rating: int | None = Field(None, ge=1, le=5, description="Оценка книги от 1 до 5")
    text: str | None = Field(None, description="Текстовый отзыв на книгу")


class ReviewReadSchema(ReviewBaseSchema):

    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)
