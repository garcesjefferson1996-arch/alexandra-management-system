from app.services.auth_service import login
from app.services.product_service import (
    list_products,
    create_product,
    get_products_grouped_by_category
)
from app.services.sale_service import register_sale
from app.services.expense_service import register_expense
from app.services.cashbox_service import close_daily_cashbox
from app.services.report_service import monthly_report
from app.services.category_service import create_category, list_categories
from app.models.sale import Sale
from app.repositories.sale_repo import get_next_sale_id
from app.services.product_service import toggle_product_status



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
            print("⚠️ No hay categorías registradas")
        else:
            print("Categorías existentes:")
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
            print("⚠️ No hay productos registrados")
        else:
            print("Productos existentes:")
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

            register_sale(sale, current_user)
            print(f"✅ Venta guardada | Total: ${sale.total:.2f}")

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

            print("\n📊 REPORTE MENSUAL (últimos 30 días)")
            print(f"Ventas totales:   ${report['total_sales']:.2f}")
            print(f"Gastos totales:   ${report['total_expenses']:.2f}")
            print(f"Ahorro (5%):      ${report['savings']:.2f}")
            print(f"Utilidad neta:    ${report['net_income']:.2f}")

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
