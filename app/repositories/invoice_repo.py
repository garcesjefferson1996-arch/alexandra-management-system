import json
import os

DATA_FILE = "app/data/invoices.json"


def load_invoices():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_invoice(invoice: dict):
    invoices = load_invoices()
    invoices.append(invoice)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(invoices, f, indent=2, ensure_ascii=False)


def get_next_invoice_number():
    invoices = load_invoices()
    return len(invoices) + 1
