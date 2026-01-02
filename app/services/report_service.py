from datetime import datetime, timedelta
from app.repositories.sale_repo import load_sales
from app.repositories.expense_repo import load_expenses

def monthly_report(days: int = 30) -> dict:
    now = datetime.now()
    start_date = now - timedelta(days=days)

    sales = load_sales()
    expenses = load_expenses()

    total_sales = 0
    total_expenses = 0

    for sale in sales:
        timestamp = sale.get("timestamp")

        if not timestamp:
            continue  # ⬅️ venta inválida, se ignora

        try:
            sale_date = datetime.fromisoformat(timestamp)
        except ValueError:
            continue

        if sale_date >= start_date:
            total_sales += sale.get("total", 0)

    for expense in expenses:
        timestamp = expense.get("timestamp")

        if not timestamp:
            continue

        try:
            expense_date = datetime.fromisoformat(timestamp)
        except ValueError:
            continue

        if expense_date >= start_date:
            total_expenses += expense.get("amount", 0)

    savings = total_sales * 0.05
    net_income = total_sales - total_expenses - savings

    return {
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "savings": savings,
        "net_income": net_income
    }
