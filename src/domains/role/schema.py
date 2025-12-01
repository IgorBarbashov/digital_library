from src.constants.user_role import UserRole
from src.domains.common.schema import BaseSchema


class RoleBaseSchema(BaseSchema):
    name: UserRole
