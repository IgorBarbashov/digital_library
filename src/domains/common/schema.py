from typing import Any

from pydantic import BaseModel, model_validator

from src.constants.order_direction import OrderDirection
from src.exceptions.entity import NoDataToPatchEntity


class BaseSchema(BaseModel):
    pass


class BasePatchSchema(BaseSchema):
    @model_validator(mode="before")
    def check_at_least_one(cls, values):
        if not values or all(v is None for v in values.values()):
            raise NoDataToPatchEntity()
        return values


class OrderBaseSchema(BaseSchema):
    order_by: Any
    order_direction: OrderDirection = OrderDirection.asc
