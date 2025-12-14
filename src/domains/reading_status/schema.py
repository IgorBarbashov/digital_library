import uuid

from pydantic import ConfigDict, Field

from src.constants.reading_status import BookReadingStatus
from src.domains.book.constants import BookOrderBy
from src.domains.common.schema import BaseSchema, OrderBaseSchema


class ReadingStatusBaseSchema(BaseSchema):
    book_id: uuid.UUID = Field(..., description="ID книги")
    status: BookReadingStatus = Field(..., description="Статус чтения книги")


class ReadingStatusCreateSchema(ReadingStatusBaseSchema):
    pass


class ReadingStatusUpdateSchema(ReadingStatusBaseSchema):
    pass


class ReadingStatusReadSchema(BaseSchema):
    status: BookReadingStatus = Field(..., description="Статус чтения книги")

    model_config = ConfigDict(from_attributes=True)


class ReadingStatusPathSchema(ReadingStatusCreateSchema):
    pass


class ReadingStatusFiltersSchema(BaseSchema):
    status: BookReadingStatus


class ReadingStatusOrderSchema(OrderBaseSchema):
    order_by: BookOrderBy = BookOrderBy.title_
