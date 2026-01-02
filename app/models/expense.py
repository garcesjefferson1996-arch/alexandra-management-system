from datetime import datetime

class Expense:
    def __init__(self, amount: float, category: str, description: str, user: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.user = user
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "user": self.user,
            "timestamp": self.timestamp
        }
