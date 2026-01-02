from app.models.product import Product
from app.repositories.product_repo import (
    load_products,
    save_all_products,
    get_next_product_id
)
from app.repositories.category_repo import load_categories
from app.services.audit_service import log_action


def list_products():
    products = load_products()
    valid_products = []

    for p in products:
        # Productos antiguos sin categoría
        if "category_id" not in p:
            continue

        if not p.get("active", True):
            continue

        valid_products.append(
            Product(
                p["id"],
                p["name"],
                p["price"],
                p["category_id"],
                p.get("active", True)
            )
        )

    return valid_products


def create_product(current_user):
    if current_user.role != "admin":
        print("❌ Solo ADMIN puede crear productos")
        return

    categories = load_categories()
    if not categories:
        print("❌ Primero debe crear categorías")
        return

    print("\n📂 CATEGORÍAS:")
    for c in categories:
        print(f"{c['id']}. {c['name']}")

    try:
        category_id = int(input("Seleccione categoría: "))
    except ValueError:
        print("❌ Categoría inválida")
        return

    if not any(c["id"] == category_id for c in categories):
        print("❌ Categoría no existe")
        return

    name = input("Nombre del producto: ").strip()
    if not name:
        print("❌ Nombre inválido")
        return

    try:
        price = float(input("Precio: $"))
    except ValueError:
        print("❌ Precio inválido")
        return

    products = load_products()

    product = Product(
        product_id=get_next_product_id(),
        name=name,
        price=price,
        category_id=category_id
    )

    products.append(product.to_dict())
    save_all_products(products)

    log_action(
        user=current_user,
        action="Creó producto",
        reason=f"{name} (${price:.2f})"
    )

    print("✅ Producto creado correctamente")
