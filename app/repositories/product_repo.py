import json
import os

DATA_FILE = "app/data/products.json"


def load_products():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_all_products(products: list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)


def get_next_product_id() -> int:
    products = load_products()
    if not products:
        return 1
    return max(p["id"] for p in products) + 1

def update_product(product_id: int, active: bool):
    products = load_products()

    for p in products:
        if p["id"] == product_id:
            p["active"] = active
            break

    save_all_products(products)