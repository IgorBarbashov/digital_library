class InactiveUser(Exception):
    def __init__(self):
        self.msg = "Inactive user"
        super().__init__(self.msg)


class BadCredentials(Exception):
    def __init__(self):
        self.msg = "Could not validate credentials"
        super().__init__(self.msg)


class IncorrectUsernamePassword(Exception):
    def __init__(self):
        self.msg = "Incorrect username or password"
        super().__init__(self.msg)
