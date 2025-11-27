import uuid


class EntityNotFound(Exception):
    def __init__(self, id: uuid.UUID, name: str = "entity"):
        self.msg = f"{name.capitalize()} {id=} not found"
        super().__init__(self.msg)
