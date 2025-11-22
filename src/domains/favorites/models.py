from __future__ import annotations

import uuid

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.user.models import User
    from src.domains.book.models import Book


class Favorites(Base, BaseModelMixin):
    __tablename__ = "favorites"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("user.id"), unique=False, index=True
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("book.id"), unique=False, index=True
    )

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    book: Mapped["Book"] = relationship("Book", back_populates="favorites")
