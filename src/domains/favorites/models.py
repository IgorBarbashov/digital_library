from __future__ import annotations

import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domains.common.models import Base, BaseModelMixin


class Favorites(Base, BaseModelMixin):
    __tablename__ = "fasvorites"

    user_id: Mapped[uuid.UUID] = mapped_column(
        String, ForeignKey("user.id"), unique=False
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        String, ForeignKey("book.id"), unique=False
    )
