from app.models.sale import Sale
from app.repositories.sale_repo import save_sale
from app.services.audit_service import log_action


def create_sale():
    """
    Crea una venta vacía
    """
    return Sale()


def add_product_to_sale(sale, product):
    """
    Agrega un producto a la venta
    """
    sale.add_product(product)


def register_sale(sale, user):
    save_sale(sale)

    log_action(
        user,
        "Creó una venta",
        f"Venta #{sale.sale_id} | Total: ${sale.total:.2f}"
    )


def delete_sale(sale_id, user):
    if user.role != "admin":
        print("❌ No autorizado.")
        return

    reason = input("Motivo de eliminación: ")
    if not reason.strip():
        print("❌ Motivo obligatorio.")
        return

    from app.repositories.sale_repo import load_sales, save_all_sales

    sales = load_sales()
    sales = [s for s in sales if s["sale_id"] != sale_id]

    save_all_sales(sales)

    log_action(
        user,
        "Eliminó una venta",
        f"Venta #{sale_id} | Motivo: {reason}"
    )

    print("✅ Venta eliminada y registrada.")