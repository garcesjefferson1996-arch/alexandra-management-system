from app.services.auth_service import login
from app.services.product_service import list_products
from app.services.sale_service import register_sale
from app.services.cashbox_service import close_daily_cashbox
from app.models.sale import Sale
from app.repositories.sale_repo import get_next_sale_id


def show_menu(products):
    print("\n☕ MENÚ - THE ALEXANDRA ☕\n")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product.name} - ${product.price:.2f}")


def create_sale(products):
    sale_id = get_next_sale_id()
    sale = Sale(sale_id)

    print("\n🛒 Nueva venta (0 para terminar)\n")

    while True:
        try:
            option = int(input("Producto #: "))

            if option == 0:
                break

            selected_product = products[option - 1]
            sale.add_product(selected_product)
            print(f"✔ Agregado: {selected_product.name}")

        except (ValueError, IndexError):
            print("❌ Opción inválida. Intenta nuevamente.")

    return sale


def main():
    current_user = login()
    if not current_user:
        return

    products = list_products()

    if not products:
        print("⚠️ No hay productos registrados.")
        return

    show_menu(products)

    sale = create_sale(products)

    if not sale.items:
        print("\n⚠️ Venta cancelada (sin productos).")
        return

    register_sale(sale, current_user)


    print(f"\n✅ Venta guardada correctamente")
    print(f"💵 Total venta: ${sale.total:.2f}")

    cashbox = close_daily_cashbox()

    print("\n📊 CIERRE DE CAJA DEL DÍA")
    print(f"Total vendido: ${cashbox.total_sales:.2f}")
    print(f"Ahorro Alexandra 💙: ${cashbox.savings:.2f}")
    print(f"Ingreso neto: ${cashbox.net_income:.2f}")


if __name__ == "__main__":
    main()
