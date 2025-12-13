import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.favorites.models import Favorites
    from src.domains.review.models import Review
    from src.domains.role.models import Role


class User(Base, BaseModelMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password_changed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("role.id", ondelete="RESTRICT"), nullable=False)
    role: Mapped[Role] = relationship("Role", back_populates="users")

    favorites: Mapped[list[Favorites]] = relationship("Favorites", back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
    )
