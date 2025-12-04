from typing import Any


class EntityNotFound(Exception):
    def __init__(self, filters: dict[str, Any], entity_name: str = "entity"):
        self.message = f"{entity_name.capitalize()} with {filters=} not found"
        super().__init__(self.message)


class EntityAlreadyExists(Exception):
    def __init__(self, filters: dict[str, Any], entity_name: str = "entity"):
        self.message = f"{entity_name.capitalize()} with {filters=} already exists"
        super().__init__(self.message)


class NoDataToPatchEntity(Exception):
    def __init__(self, entity_name: str = "entity"):
        self.message = f"No data to update {entity_name.capitalize()}"
        super().__init__(self.message)
