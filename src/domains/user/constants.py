from enum import StrEnum

from sqlalchemy.orm import InstrumentedAttribute

from src.domains.user.models import User


class UserOrderBy(StrEnum):
    username = "username"
    first_name = "first_name"
    last_name = "last_name"
    email = "email"
    create_at = "create_at"


ORDER_COLUMN_MAP: dict[UserOrderBy, InstrumentedAttribute] = {
    UserOrderBy.username: User.username,
    UserOrderBy.first_name: User.first_name,
    UserOrderBy.last_name: User.last_name,
    UserOrderBy.email: User.email,
    UserOrderBy.create_at: User.create_at,
}
