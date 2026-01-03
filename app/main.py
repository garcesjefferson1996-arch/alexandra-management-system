from app.models.customer import Customer
from app.services.invoice_service import generate_invoice
from app.services.auth_service import login
from app.services.product_service import (
    list_products,
    create_product,
    get_products_grouped_by_category,
    toggle_product_status
)
from app.services.sale_service import register_sale
from app.services.expense_service import register_expense
from app.services.cashbox_service import close_daily_cashbox
from app.services.report_service import monthly_report
from app.services.category_service import create_category
from app.services.order_service import (
    create_order,
    add_product_to_order,
    close_order_and_generate_sale,
    list_open_orders_by_table
)
from app.services.table_service import list_tables, create_table


# =========================
# PRODUCTOS
# =========================

def show_products_by_category(grouped_products):
    print("\n☕ MENÚ - THE ALEXANDRA ☕\n")
    index = 1
    index_map = {}

    for data in grouped_products.values():
        if not data["products"]:
            continue

        print(f"\n📂 {data['name']}")
        for product in data["products"]:
            print(f"{index}. {product.name} - ${product.price:.2f}")
            index_map[index] = product
            index += 1

    return index_map


def add_products_to_order(order_id):
    grouped = get_products_grouped_by_category()
    index_map = show_products_by_category(grouped)

    print("\n0. Terminar pedido")

    while True:
        try:
            option = int(input("Producto #: "))
            if option == 0:
                break

            product = index_map.get(option)
            if not product:
                print("❌ Producto inválido")
                continue

            add_product_to_order(order_id, product.id)
            print(f"✔ Agregado: {product.name}")

        except ValueError:
            print("❌ Opción inválida")


# =========================
# PAGOS Y FACTURACIÓN
# =========================

def process_payment(sale):
    print("\n💳 MÉTODO DE PAGO")
    print("1. Efectivo")
    print("2. Tarjeta")
    print("3. Transferencia")

    option = input("Seleccione método: ")

    methods = {
        "1": "EFECTIVO",
        "2": "TARJETA",
        "3": "TRANSFERENCIA"
    }

    method = methods.get(option)
    if not method:
        print("❌ Método inválido")
        return False

    try:
        paid = float(input("Monto pagado: $"))
    except ValueError:
        print("❌ Monto inválido")
        return False

    if paid < sale.total:
        print("❌ El monto no cubre el total")
        return False

    sale.set_payment(method, paid)
    print(f"✔ Pago registrado | Vuelto: ${sale.change:.2f}")
    return True


def process_invoice(sale):
    option = input("\n¿Desea factura? (s/n): ").lower()
    if option != "s":
        return

    print("\n🧾 DATOS DEL CLIENTE")
    name = input("Nombre / Razón social: ")
    document = input("Cédula o RUC: ")
    email = input("Email (opcional): ")

    customer = Customer(name, document, email)
    sale.attach_customer(customer.to_dict())

    invoice = generate_invoice(sale, customer.to_dict())
    sale.mark_invoiced(invoice.invoice_number)

    print(f"🧾 Factura interna generada N° {invoice.invoice_number}")


# =========================
# ÓRDENES
# =========================

def select_order_type():
    print("\n🧾 TIPO DE PEDIDO")
    print("1. Mesa")
    print("2. Para llevar")
    print("3. Delivery")

    option = input("Seleccione: ")

    if option == "1":
        return "DINE_IN"
    elif option == "2":
        return "TAKEAWAY"
    elif option == "3":
        return "DELIVERY"
    else:
        print("❌ Opción inválida")
        return None


def select_table():
    tables = list_tables()
    free_tables = [t for t in tables if t["status"] == "FREE"]

    if not free_tables:
        print("❌ No hay mesas libres")
        return None

    print("\n🪑 MESAS DISPONIBLES")
    for t in free_tables:
        print(f"{t['table_id']}. {t['name']}")

    try:
        return int(input("Seleccione mesa: "))
    except ValueError:
        return None


def new_order_flow(current_user):
    order_type = select_order_type()
    if not order_type:
        return

    table_id = None
    customer = None

    if order_type == "DINE_IN":
        table_id = select_table()
        if not table_id:
            return

    if order_type == "DELIVERY":
        print("\n🛵 DATOS DELIVERY")
        customer = {
            "name": input("Nombre: "),
            "phone": input("Teléfono: "),
            "address": input("Dirección: ")
        }

    order = create_order(order_type, table_id, customer)
    add_products_to_order(order.order_id)

    confirm = input("\n¿Cobrar y cerrar pedido? (s/n): ").lower()
    if confirm != "s":
        print("⏸ Pedido guardado")
        return

    sale = close_order_and_generate_sale(order.order_id)

    if not process_payment(sale):
        print("❌ Pago no registrado")
        return

    process_invoice(sale)
    register_sale(sale, current_user)

    print("\n✅ Venta finalizada correctamente")
    print(f"💵 Total: ${sale.total:.2f}")


# =========================
# PEDIDOS ABIERTOS (NUEVO)
# =========================

def show_open_orders_interactive(current_user):
    data = list_open_orders_by_table()
    index_map = {}
    index = 1

    print("\n📌 PEDIDOS ABIERTOS")

    for table_id, orders in data["DINE_IN"].items():
        for o in orders:
            print(f"{index}. Mesa {table_id} → Pedido #{o['order_id']} | ${o['total']:.2f}")
            index_map[index] = o
            index += 1

    for o in data["TAKEAWAY"]:
        print(f"{index}. Para llevar → Pedido #{o['order_id']} | ${o['total']:.2f}")
        index_map[index] = o
        index += 1

    for o in data["DELIVERY"]:
        print(f"{index}. Delivery → Pedido #{o['order_id']} | ${o['total']:.2f}")
        index_map[index] = o
        index += 1

    if not index_map:
        print("📭 No hay pedidos abiertos")
        return

    try:
        choice = int(input("\nSeleccione pedido (0 volver): "))
        if choice == 0:
            return

        order = index_map.get(choice)
        if not order:
            print("❌ Pedido inválido")
            return

        print("\n1. Agregar productos")
        print("2. Cobrar y cerrar")
        print("0. Volver")

        action = input("Seleccione: ")

        if action == "1":
            add_products_to_order(order["order_id"])

        elif action == "2":
            sale = close_order_and_generate_sale(order["order_id"])

            if not process_payment(sale):
                return

            process_invoice(sale)
            register_sale(sale, current_user)

            print("\n✅ Pedido cerrado correctamente")

    except ValueError:
        print("❌ Entrada inválida")


# =========================
# MENÚ PRINCIPAL
# =========================

def main_menu(is_admin):
    print("\n📋 MENÚ PRINCIPAL")
    print("1. Nuevo pedido")
    print("2. Cierre de caja")

    if is_admin:
        print("3. Registrar gasto (ADMIN)")
        print("4. Reporte mensual (ADMIN)")
        print("5. Gestionar categorías (ADMIN)")
        print("6. Gestionar productos (ADMIN)")
        print("7. Gestionar mesas (ADMIN)")
        print("8. Ver pedidos abiertos")

    print("0. Salir")


def table_menu(current_user):
    while True:
        print("\n🪑 GESTIÓN DE MESAS")

        tables = list_tables()
        if not tables:
            print("⚠️ No hay mesas creadas")
        else:
            for t in tables:
                print(f"{t['table_id']}. {t['name']} - {t['status']}")

        print("\n1. Agregar mesa")
        print("0. Volver")

        option = input("Seleccione una opción: ")

        if option == "1":
            name = input("Nombre de la mesa: ")
            create_table(name, current_user)
            print("✅ Mesa creada correctamente")

        elif option == "0":
            break


def main():
    current_user = login()
    if not current_user:
        return

    is_admin = current_user.role == "admin"

    while True:
        main_menu(is_admin)
        option = input("\nSeleccione una opción: ").strip()

        if option == "1":
            new_order_flow(current_user)

        elif option == "2":
            cashbox = close_daily_cashbox(current_user)
            print("\n📊 CIERRE DE CAJA")
            print(f"Total vendido: ${cashbox.total_sales:.2f}")
            print(f"Ahorro Alexandra 💙: ${cashbox.savings:.2f}")
            print(f"Ingreso neto: ${cashbox.net_income:.2f}")

        elif option == "3" and is_admin:
            register_expense(current_user)

        elif option == "4" and is_admin:
            report = monthly_report()
            print("\n📊 REPORTE MENSUAL")
            print(f"Ventas: ${report['total_sales']:.2f}")
            print(f"Gastos: ${report['total_expenses']:.2f}")
            print(f"Ahorro: ${report['savings']:.2f}")
            print(f"Utilidad: ${report['net_income']:.2f}")

        elif option == "5" and is_admin:
            create_category(current_user)

        elif option == "6" and is_admin:
            create_product(current_user)

        elif option == "7" and is_admin:
            table_menu(current_user)

        elif option == "8":
            show_open_orders_interactive(current_user)

        elif option == "0":
            print("👋 Hasta luego")
            break

        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    main()
