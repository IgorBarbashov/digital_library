from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domains.common.models import Base, BaseModelMixin

if TYPE_CHECKING:
    from src.domains.book.models import Book


class Category(Base, BaseModelMixin):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="category")
