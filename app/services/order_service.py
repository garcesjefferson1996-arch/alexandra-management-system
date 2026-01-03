from app.models.order import Order
from app.repositories.order_repo import (
    load_orders,
    save_orders,
    get_next_order_id
)
from app.services.table_service import (
    list_free_tables,
    occupy_table,
    free_table
)
from app.services.product_service import list_products
from app.models.sale import Sale
from app.repositories.sale_repo import get_next_sale_id
from app.services.sale_service import register_sale
from app.models.user import User


# =========================
# LISTAR ÓRDENES
# =========================

def list_orders():
    return load_orders()


# =========================
# CREAR ORDEN
# =========================

def create_order(order_type: str, table_id: int | None = None, customer: dict | None = None):
    orders = load_orders()

    # Validación de mesas
    if order_type == "DINE_IN":
        free_tables = list_free_tables()
        free_table_ids = [t["table_id"] for t in free_tables]

        if not free_table_ids:
            print("❌ No hay mesas libres")
            return None

        if table_id not in free_table_ids:
            print("❌ Mesa inválida o no disponible")
            return None

        occupy_table(table_id)

    order = Order(
        order_id=get_next_order_id(),
        order_type=order_type,
        table_id=table_id,
        customer=customer
    )

    orders.append(order.to_dict())
    save_orders(orders)

    return order


# =========================
# AGREGAR PRODUCTO A ORDEN
# =========================

def add_product_to_order(order_id: int, product_id: int):
    orders = load_orders()
    products = list_products()

    product_map = {p.id: p for p in products}

    for order in orders:
        if order["order_id"] == order_id and order["status"] == "OPEN":
            product = product_map.get(product_id)

            if not product or not product.active:
                return False, "Producto inválido o inactivo"

            order["items"].append({
                "name": product.name,
                "price": product.price
            })
            order["total"] += product.price

            save_orders(orders)
            return True, order

    return False, "Orden no encontrada o cerrada"


# =========================
# CERRAR ORDEN (SIN VENTA)
# =========================

def close_order(order_id: int):
    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id and order["status"] == "OPEN":
            order["status"] = "CLOSED"

            if order["type"] == "DINE_IN" and order["table_id"]:
                free_table(order["table_id"])

            save_orders(orders)
            return order

    return None


def list_open_orders():
    orders = load_orders()
    return [o for o in orders if o["status"] == "OPEN"]


def list_open_orders_by_table():
    orders = load_orders()

    result = {
        "DINE_IN": {},
        "TAKEAWAY": [],
        "DELIVERY": []
    }

    for order in orders:
        if order["status"] != "OPEN":
            continue

        if order["type"] == "DINE_IN":
            table_id = order["table_id"]
            result["DINE_IN"].setdefault(table_id, []).append(order)

        elif order["type"] == "TAKEAWAY":
            result["TAKEAWAY"].append(order)

        elif order["type"] == "DELIVERY":
            result["DELIVERY"].append(order)

    return result



# =========================
# CERRAR ORDEN Y GENERAR VENTA
# =========================

def close_order_and_generate_sale(order_id: int):
    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id and order["status"] == "OPEN":

            # Crear venta
            sale = Sale(get_next_sale_id())

            for item in order["items"]:
                sale.items.append(item)
                sale.total += item["price"]

            # Usuario sistema (temporal, luego será auth real)
            system_user = User("system", "api", "admin")

            register_sale(sale, system_user)

            # Cerrar orden
            order["status"] = "CLOSED"

            # Liberar mesa
            if order["type"] == "DINE_IN" and order["table_id"]:
                free_table(order["table_id"])

            save_orders(orders)
            return sale

    return None

def list_open_orders():
    orders = load_orders()
    return [o for o in orders if o["status"] == "OPEN"]
