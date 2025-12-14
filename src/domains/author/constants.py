from enum import StrEnum

from sqlalchemy.orm import InstrumentedAttribute

from src.domains.author.models import Author


class AuthorOrderBy(StrEnum):
    last_name = "last_name"
    create_at = "create_at"


ORDER_COLUMN_MAP: dict[AuthorOrderBy, InstrumentedAttribute] = {
    AuthorOrderBy.last_name: Author.last_name,
    AuthorOrderBy.create_at: Author.create_at,
}
