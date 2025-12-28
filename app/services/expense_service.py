from app.repositories.expense_repo import save_expense


def register_expense(description: str, amount: float) -> None:
    expense = {
        "description": description,
        "amount": amount
    }
    save_expense(expense)
