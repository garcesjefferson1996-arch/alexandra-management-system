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
from app.services.category_service import create_category, list_categories
from app.models.sale import Sale
from app.repositories.sale_repo import get_next_sale_id


# =========================
# VENTAS
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


def create_sale(index_map):
    sale_id = get_next_sale_id()
    sale = Sale(sale_id)

    print("\n🛒 Nueva venta (0 para terminar)\n")

    while True:
        try:
            option = int(input("Producto #: "))
            if option == 0:
                break

            product = index_map.get(option)
            if not product:
                print("❌ Opción inválida")
                continue

            sale.add_product(product)
            print(f"✔ Agregado: {product.name}")

        except ValueError:
            print("❌ Opción inválida")

    return sale


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
# MENÚS
# =========================

def main_menu(is_admin: bool):
    print("\n📋 MENÚ PRINCIPAL")
    print("1. Registrar venta")
    print("2. Cierre de caja")

    if is_admin:
        print("3. Registrar gasto (ADMIN)")
        print("4. Reporte mensual (ADMIN)")
        print("5. Gestionar categorías (ADMIN)")
        print("6. Gestionar productos (ADMIN)")

    print("0. Salir")


def category_menu(current_user):
    while True:
        print("\n📂 GESTIÓN DE CATEGORÍAS")
        categories = list_categories()

        if not categories:
            print("⚠️ No hay categorías")
        else:
            for c in categories:
                print(f"- {c['name']}")

        print("\n1. Agregar categoría")
        print("0. Volver")

        option = input("Seleccione una opción: ")

        if option == "1":
            create_category(current_user)
        elif option == "0":
            break
        else:
            print("❌ Opción inválida")


def product_menu(current_user):
    while True:
        print("\n📦 GESTIÓN DE PRODUCTOS")

        products = list_products()
        if not products:
            print("⚠️ No hay productos")
        else:
            for p in products:
                print(f"- {p.name} (${p.price:.2f})")

        print("\n1. Agregar producto")
        print("2. Activar / Desactivar producto")
        print("0. Volver")

        option = input("Seleccione una opción: ")

        if option == "1":
            create_product(current_user)
        elif option == "2":
            toggle_product_status(current_user)
        elif option == "0":
            break
        else:
            print("❌ Opción inválida")


# =========================
# MAIN
# =========================

def main():
    current_user = login()
    if not current_user:
        return

    is_admin = current_user.role == "admin"

    while True:
        main_menu(is_admin)
        option = input("\nSeleccione una opción: ")

        if option == "1":
            grouped = get_products_grouped_by_category()
            if not grouped:
                print("⚠️ No hay productos disponibles")
                continue

            index_map = show_products_by_category(grouped)
            sale = create_sale(index_map)

            if not sale.items:
                print("⚠️ Venta cancelada")
                continue

            if not process_payment(sale):
                print("⚠️ Pago no registrado. Venta cancelada.")
                continue

            process_invoice(sale)

            register_sale(sale, current_user)

            print("\n✅ Venta guardada correctamente")
            print(f"💵 Total: ${sale.total:.2f}")
            print(f"💳 Método: {sale.payment_method}")
            print(f"💰 Pagó: ${sale.paid_amount:.2f}")
            print(f"🔁 Vuelto: ${sale.change:.2f}")

            if sale.invoice_id:
                print(f"🧾 Factura N° {sale.invoice_id}")

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
            print(f"Ventas:   ${report['total_sales']:.2f}")
            print(f"Gastos:   ${report['total_expenses']:.2f}")
            print(f"Ahorro:   ${report['savings']:.2f}")
            print(f"Utilidad: ${report['net_income']:.2f}")

        elif option == "5" and is_admin:
            category_menu(current_user)

        elif option == "6" and is_admin:
            product_menu(current_user)

        elif option == "0":
            print("👋 Hasta luego")
            break

        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    main()
