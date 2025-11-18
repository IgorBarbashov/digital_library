import uuid
from datetime import datetime

from pydantic import BaseModel


class BaseEntity(BaseModel):
    pass


class BaseEntityResponse(BaseEntity):
    id: uuid.UUID
    create_at: datetime
    update_at: datetime
