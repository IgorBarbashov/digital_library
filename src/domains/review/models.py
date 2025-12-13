from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.domains.common.models import Base, BaseModelMixin


class Review(Base, BaseModelMixin):
    __tablename__ = "review"

    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    book_id = Column(String, ForeignKey("book.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=True)

    __table_args__ = (CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
