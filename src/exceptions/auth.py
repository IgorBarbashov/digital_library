class InactiveUser(Exception):
    def __init__(self):
        self.message = "Inactive user"
        super().__init__(self.message)


class BadCredentials(Exception):
    def __init__(self):
        self.message = "Could not validate credentials"
        super().__init__(self.message)


class IncorrectUsernamePassword(Exception):
    def __init__(self):
        self.message = "Incorrect username or password"
        super().__init__(self.message)


class AdminRoleRequired(Exception):
    def __init__(self):
        self.message = "Admin role required"
        super().__init__(self.message)
