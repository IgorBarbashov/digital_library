import uuid


class EntityNotFound(Exception):
    def __init__(self, id: uuid.UUID, entity_name: str = "entity"):
        self.msg = f"{entity_name.capitalize()} {id=} not found"
        super().__init__(self.msg)


class EntityAlreadyExists(Exception):
    def __init__(self, name: str, entity_name: str = "entity"):
        self.msg = f"{entity_name.capitalize()} with {name=} already exists"
        super().__init__(self.msg)
