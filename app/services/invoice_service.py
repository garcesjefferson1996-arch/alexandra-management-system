from app.models.invoice import Invoice
from app.repositories.invoice_repo import (
    save_invoice,
    get_next_invoice_number
)

IVA_RATE = 0.12


def generate_invoice(sale, customer: dict):
    """
    Genera una factura interna (lista para SRI)
    """

    subtotal = round(sale.total / (1 + IVA_RATE), 2)
    iva = round(subtotal * IVA_RATE, 2)

    invoice = Invoice(
        invoice_number=get_next_invoice_number(),
        sale_id=sale.sale_id,
        customer=customer,
        subtotal=subtotal,
        iva=iva,
        total=sale.total
    )

    save_invoice(invoice.to_dict())
    return invoice
