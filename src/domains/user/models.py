from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.role.models import Role


class User(Base, BaseModelMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password_changed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=None
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("role.id"), nullable=False, ondelete="RESTRICT"
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users")
