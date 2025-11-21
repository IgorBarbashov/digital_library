from __future__ import annotations

import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domains.common.models import Base, BaseModelMixin


class Book(Base, BaseModelMixin):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        String, ForeignKey("author.id"), nullable=False, unique=False
    )
    genre_id: Mapped[uuid.UUID] = mapped_column(
        String, ForeignKey("genre.id"), nullable=False, unique=False
    )
