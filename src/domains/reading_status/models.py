import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.constants.reading_status import BookReadingStatus
from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.book.models import Book
    from src.domains.user.models import User


class ReadingStatus(Base, BaseModelMixin):
    __tablename__ = "reading_status"

    __table_args__ = (UniqueConstraint("user_id", "book_id", name="uc_user_book"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    book_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("book.id", ondelete="CASCADE"),
        nullable=False,
    )

    status: Mapped[BookReadingStatus | None] = mapped_column(Integer, nullable=True)

    users: Mapped["User"] = relationship("User", back_populates="reading_books")

    books: Mapped["Book"] = relationship("Book", back_populates="reading_users")
