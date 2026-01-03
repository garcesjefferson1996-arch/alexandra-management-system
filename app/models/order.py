from datetime import datetime

class Order:
    def __init__(
        self,
        order_id: int,
        order_type: str,        # DINE_IN | TAKEAWAY | DELIVERY
        table_id: int | None = None,
        customer: dict | None = None
    ):
        self.order_id = order_id
        self.type = order_type
        self.table_id = table_id
        self.customer = customer
        self.items = []
        self.total = 0.0
        self.status = "OPEN"
        self.timestamp = datetime.now().isoformat()

    def add_product(self, product):
        self.items.append({
            "name": product.name,
            "price": product.price
        })
        self.total += product.price

    def close(self):
        self.status = "CLOSED"

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "type": self.type,
            "table_id": self.table_id,
            "customer": self.customer,
            "items": self.items,
            "total": self.total,
            "status": self.status,
            "timestamp": self.timestamp
        }
