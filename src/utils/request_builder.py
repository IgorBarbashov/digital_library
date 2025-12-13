from typing import Any, TypeVar

from sqlalchemy import Select
from sqlalchemy.orm import InstrumentedAttribute

from src.constants.order_direction import OrderDirection
from src.domains.common.schema import OrderBaseSchema

TRow = TypeVar("TRow", bound=tuple)


def apply_ordering(
    stmt: Select[TRow],
    order: OrderBaseSchema,
    order_by_dict: dict[Any, InstrumentedAttribute],
) -> Select[TRow]:
    column = order_by_dict[order.order_by]
    column = column.desc() if order.order_direction == OrderDirection.desc else column.asc()
    return stmt.order_by(column)
