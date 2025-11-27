from pydantic import BaseModel, model_validator

from src.exceptions.entity import NoDataToUpdate


class BaseSchema(BaseModel):
    pass


class BaseUpdateSchema(BaseSchema):
    @model_validator(mode="before")
    def check_at_least_one(cls, values):
        if not values or all(v is None for v in values.values()):
            raise NoDataToUpdate()
        return values
