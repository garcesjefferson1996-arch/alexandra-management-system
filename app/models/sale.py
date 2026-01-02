from datetime import datetime


class Sale:
    def __init__(self, sale_id: int):
        self.sale_id = sale_id
        self.items = []
        self.total = 0.0
        self.timestamp = datetime.now().isoformat()

        # 🔽 NUEVO (facturación y pago)
        self.customer = None
        self.payment_method = None
        self.paid_amount = 0.0
        self.change = 0.0
        self.invoice_id = None
        self.status = "DRAFT"  # DRAFT | INVOICED

    def add_product(self, product):
        self.items.append({
            "name": product.name,
            "price": product.price
        })
        self.total += product.price

    def set_payment(self, method: str, paid_amount: float):
        self.payment_method = method
        self.paid_amount = paid_amount
        self.change = round(paid_amount - self.total, 2)

    def attach_customer(self, customer: dict):
        self.customer = customer

    def mark_invoiced(self, invoice_id: int):
        self.invoice_id = invoice_id
        self.status = "INVOICED"

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "items": self.items,
            "total": round(self.total, 2),
            "timestamp": self.timestamp,
            "customer": self.customer,
            "payment_method": self.payment_method,
            "paid_amount": self.paid_amount,
            "change": self.change,
            "invoice_id": self.invoice_id,
            "status": self.status
        }
