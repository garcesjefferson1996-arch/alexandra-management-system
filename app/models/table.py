class Table:
    def __init__(self, table_id: int, name: str, status: str = "FREE"):
        self.table_id = table_id
        self.name = name
        self.status = status  # FREE | OCCUPIED

    def occupy(self):
        self.status = "OCCUPIED"

    def free(self):
        self.status = "FREE"

    def to_dict(self):
        return {
            "table_id": self.table_id,
            "name": self.name,
            "status": self.status
        }
