class Customer:
    def __init__(self, name: str, document: str, email: str = ""):
        self.name = name
        self.document = document  # Cédula o RUC
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "document": self.document,
            "email": self.email
        }
