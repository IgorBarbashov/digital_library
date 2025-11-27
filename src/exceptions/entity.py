import uuid


class EntityNotFound(Exception):
    def __init__(self, msg: str = "Entity not found"):
        super().__init__(msg)


class AuthorNotFound(EntityNotFound):
    def __init__(self, author_id: uuid.UUID):
        self.msg = f"Author {author_id=} not found"
        super().__init__(self.msg)


class NoDataToUpdate(Exception):
    def __init__(self, msg: str = "No data to update"):
        super().__init__(msg)
