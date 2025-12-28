import json
import os

DATA_FILE = "app/data/sales.json"


def load_sales():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_sale(sale):
    sales = load_sales()
    sales.append(sale.to_dict())

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, indent=4, ensure_ascii=False)


def get_next_sale_id():
    sales = load_sales()
    return len(sales) + 1

def save_all_sales(sales):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, indent=4, ensure_ascii=False)

