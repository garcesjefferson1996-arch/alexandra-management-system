class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password   # luego la encriptamos
        self.role = role           # admin | cashier

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }
