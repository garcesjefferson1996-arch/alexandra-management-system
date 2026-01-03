import json
import os

DATA_FILE = "app/data/tables.json"


def load_tables():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_tables(tables: list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)


def get_next_table_id():
    tables = load_tables()
    return len(tables) + 1
