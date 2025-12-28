import json

DATA_FILE = "app/data/expenses.json"


def load_expenses() -> list:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except FileNotFoundError:
        return []


def save_expense(expense: dict) -> None:
    expenses = load_expenses()
    expenses.append(expense)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)
