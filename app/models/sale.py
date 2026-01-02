from datetime import datetime

class Sale:
    def __init__(self, sale_id: int):
        self.sale_id = sale_id
        self.items = []
        self.total = 0.0
        self.timestamp = datetime.now().isoformat()

    def add_product(self, product):
        self.items.append({
            "name": product.name,
            "price": product.price
        })
        self.total += product.price

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "items": self.items,
            "total": self.total,
            "timestamp": self.timestamp
        }
