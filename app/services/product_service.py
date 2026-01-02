from app.models.product import Product
from app.repositories.product_repo import (
    load_products,
    save_all_products,
    get_next_product_id
)
from app.repositories.category_repo import load_categories
from app.services.audit_service import log_action
from app.repositories.category_repo import load_categories
from app.repositories.product_repo import update_product



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

def get_products_grouped_by_category():
    products = load_products()
    categories = load_categories()

    grouped = {}

    # Inicializar categorías
    for c in categories:
        grouped[c["id"]] = {
            "name": c["name"],
            "products": []
        }

    # Asignar productos a su categoría
    for p in products:
        if not p.get("active", True):
            continue

        category_id = p.get("category_id")
        if category_id in grouped:
            grouped[category_id]["products"].append(
                Product(
                    p["id"],
                    p["name"],
                    p["price"],
                    p["category_id"],
                    p.get("active", True)
                )
            )

    return grouped


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


def toggle_product_status(current_user):
    if current_user.role != "admin":
        print("❌ Solo ADMIN puede modificar productos")
        return

    products = load_products()
    if not products:
        print("⚠️ No hay productos")
        return

    print("\n📦 PRODUCTOS:")
    for p in products:
        status = "✅ Activo" if p.get("active", True) else "❌ Inactivo"
        print(f"{p['id']}. {p['name']} - {status}")

    try:
        product_id = int(input("ID del producto: "))
    except ValueError:
        print("❌ ID inválido")
        return

    for p in products:
        if p["id"] == product_id:
            new_status = not p.get("active", True)
            update_product(product_id, new_status)

            action = "Activó producto" if new_status else "Desactivó producto"

            log_action(
                user=current_user,
                action=action,
                reason=p["name"]
            )

            print(f"✅ Producto {'activado' if new_status else 'desactivado'}")
            return

    print("❌ Producto no encontrado")
