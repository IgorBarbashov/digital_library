from typing import Any


class EntityNotFound(Exception):
    def __init__(self, filters: dict[str, Any], entity_name: str = "entity"):
        self.msg = f"{entity_name.capitalize()} with filters {filters=} not found"
        super().__init__(self.msg)


class EntityAlreadyExists(Exception):
    def __init__(self, filters: dict[str, Any], entity_name: str = "entity"):
        self.msg = f"{entity_name.capitalize()} with filters {filters} already exists"
        super().__init__(self.msg)


class NoDataToUpdateEntityError(Exception):
    def __init__(self, msg: str = "No data to update"):
        super().__init__(msg)
