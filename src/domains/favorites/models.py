from __future__ import annotations

import uuid

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.user.models import User
    from src.domains.book.models import Book


class Favorites(Base, BaseModelMixin):
    __tablename__ = "favorites"

    __table_args__ = (
        # При удалении книги или пользователя будет автоматически удалена запись из favorites
        ForeignKeyConstraint(["user_id"], ["user.id"], name="fk_favorite_user", ondelete="CASCADE"),
        ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
            name="fk_favorite_book",
            ondelete="CASCADE",
        ),
        # Один пользователь — одна запись на книгу
        UniqueConstraint("user_id", "book_id", name="uc_user_book"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    book_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)

    users: Mapped["User"] = relationship("User", back_populates="favorites")
    books: Mapped["Book"] = relationship("Book", back_populates="favorites")
