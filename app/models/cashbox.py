from datetime import date


class CashBox:
    def __init__(self, total_sales: float, total_expenses: float):
        self.date = date.today().isoformat()
        self.total_sales = total_sales
        self.total_expenses = total_expenses

        # Ahorro automático Alexandra 💙 (5%)
        self.savings = total_sales * 0.05

        # Ingreso real del día
        self.net_income = total_sales - total_expenses - self.savings

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "total_sales": self.total_sales,
            "total_expenses": self.total_expenses,
            "savings": self.savings,
            "net_income": self.net_income
        }
