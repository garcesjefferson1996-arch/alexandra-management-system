import json
import os

DATA_FILE = "app/data/orders.json"


def load_orders():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_orders(orders: list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)


def get_next_order_id():
    orders = load_orders()
    return len(orders) + 1
