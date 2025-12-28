from app.repositories.sale_repo import load_sales
from app.repositories.expense_repo import load_expenses
from app.models.cashbox import CashBox


def close_daily_cashbox() -> CashBox:
    """
    Calcula el cierre de caja del día:
    - Total de ventas
    - Total de egresos
    - Ahorro automático
    - Ingreso neto
    """

    sales = load_sales()
    expenses = load_expenses()

    total_sales = sum(sale["total"] for sale in sales)
    total_expenses = sum(expense["amount"] for expense in expenses)

    return CashBox(
        total_sales=total_sales,
        total_expenses=total_expenses
    )

