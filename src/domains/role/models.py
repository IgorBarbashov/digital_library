from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.user.models import User


class Role(Base, BaseModelMixin):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    users: Mapped[List["User"]] = relationship("User", back_populates="role")
