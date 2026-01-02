class Category:
    def __init__(self, category_id: int, name: str):
        self.id = category_id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
