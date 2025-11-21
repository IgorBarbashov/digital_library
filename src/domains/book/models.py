from __future__ import annotations

import uuid

from sqlalchemy import String, ForeignKey, types
from sqlalchemy.orm import Mapped, mapped_column

from src.domains.common.models import Base, BaseModelMixin


class Book(Base, BaseModelMixin):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID, ForeignKey("author.id"), nullable=False, unique=False
    )
    genre_id: Mapped[uuid.UUID] = mapped_column(
        types.UUID, ForeignKey("genre.id"), nullable=False, unique=False
    )
