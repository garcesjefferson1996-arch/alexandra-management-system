import json
from app.models.product import Product

DATA_FILE = "app/data/products.json"


def get_all_products():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = []
    for item in data:
        products.append(
            Product(item["id"], item["name"], item["price"])
        )

    return products
