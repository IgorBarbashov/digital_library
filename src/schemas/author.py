import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    create_at: datetime
    update_at: datetime


class AuthorResponse(AuthorBase):
    uuid: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
