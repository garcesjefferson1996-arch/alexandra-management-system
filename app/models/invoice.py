from datetime import datetime

class Invoice:
    def __init__(
        self,
        invoice_number: int,
        sale_id: int,
        customer: dict,
        subtotal: float,
        iva: float,
        total: float
    ):
        self.invoice_number = invoice_number
        self.sale_id = sale_id
        self.customer = customer
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.date = datetime.now().isoformat()
        self.status = "PENDING_SRI"  # listo para integrar SRI

    def to_dict(self):
        return self.__dict__
