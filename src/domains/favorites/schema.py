import uuid
from src.domains.common.schema import BaseSchema


class FavoriteBase(BaseSchema):
    user_id: uuid.UUID
    book_id: uuid.UUID


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteUpdate(FavoriteBase):
    pass
