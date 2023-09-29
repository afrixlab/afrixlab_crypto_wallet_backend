from .base import BaseEnum


class UserAccountType(BaseEnum):
    SUPER_ADMINISTRATOR = "SUPER_ADMINISTRATOR"
    ADMINISTRATOR = "ADMINISTRATOR"
    USER = "REGULAR_USER"
