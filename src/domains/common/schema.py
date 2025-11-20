import uuid
from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    pass


class BaseSchema(Base):
    id: uuid.UUID
    create_at: datetime
    update_at: datetime
