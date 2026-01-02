from app.repositories.sale_repo import load_sales
from app.repositories.expense_repo import load_expenses
from app.models.cashbox import CashBox
from app.services.audit_service import log_action


def close_daily_cashbox(user):
    """
    Calcula el cierre de caja del día:
    - Total de ventas
    - Total de egresos
    - Ahorro automático
    - Ingreso neto
    - Registra auditoría
    """

    sales = load_sales()
    expenses = load_expenses()

    total_sales = sum(sale["total"] for sale in sales)
    total_expenses = sum(expense["amount"] for expense in expenses)

    cashbox = CashBox(
        total_sales=total_sales,
        total_expenses=total_expenses
    )

    # 🔐 AUDITORÍA DEL CIERRE DE CAJA
    log_action(
        user=user,
        action="Cierre de caja",
        reason=f"Ventas: ${cashbox.total_sales:.2f} | Gastos: ${cashbox.total_expenses:.2f} | Neto: ${cashbox.net_income:.2f}"
    )

    return cashbox
