import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_mixin, mapped_column


class Base(DeclarativeBase):
    pass


@declarative_mixin
class CreatedUpdatedColumnsMixin:
    create_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=func.now(),
    )


@declarative_mixin
class BaseModelMixin(CreatedUpdatedColumnsMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
