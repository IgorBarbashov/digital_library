import uuid
from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    pass


class BaseEntity(Base):
    id: uuid.UUID
    create_at: datetime
    update_at: datetime
