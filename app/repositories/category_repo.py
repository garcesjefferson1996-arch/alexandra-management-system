import json
import os

DATA_FILE = "app/data/categories.json"


def load_categories() -> list:
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_all_categories(categories: list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)


def get_next_category_id() -> int:
    categories = load_categories()
    if not categories:
        return 1
    return max(c["id"] for c in categories) + 1

