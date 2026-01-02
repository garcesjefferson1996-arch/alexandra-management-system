class Product:
    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        category_id: int,
        active: bool = True
    ):
        self.id = product_id
        self.name = name
        self.price = price
        self.category_id = category_id
        self.active = active

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category_id": self.category_id,
            "active": self.active
        }
