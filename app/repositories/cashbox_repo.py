import json
from app.models.cashbox import CashBox

DATA_FILE = "app/data/cashbox.json"

def save_cashbox(cashbox: CashBox):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            records = json.loads(content) if content else []
    except FileNotFoundError:
        records = []

    records.append(cashbox.to_dict())

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
