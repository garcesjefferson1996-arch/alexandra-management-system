from datetime import datetime


class Sale:
    def __init__(self, sale_id: int):
        self.sale_id = sale_id
        self.date = datetime.now().isoformat()
        self.items = []
        self.total = 0.0

    def add_product(self, product):
        self.items.append(product)
        self.total += product.price

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "date": self.date,
            "items": [
                {"name": p.name, "price": p.price} for p in self.items
            ],
            "total": self.total
        }
