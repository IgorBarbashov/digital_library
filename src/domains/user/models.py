from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domains.common.models import Base, BaseModelMixin


class Genre(Base, BaseModelMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
