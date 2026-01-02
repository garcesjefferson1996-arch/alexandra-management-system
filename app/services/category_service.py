from app.models.category import Category
from app.repositories.category_repo import (
    load_categories,
    save_all_categories,
    get_next_category_id
)
from app.services.audit_service import log_action


def create_category(current_user):
    if current_user.role != "admin":
        print("❌ Solo ADMIN puede crear categorías")
        return

    name = input("Nombre de la categoría: ").strip()
    if not name:
        print("❌ Nombre inválido")
        return

    categories = load_categories()

    if any(c["name"].lower() == name.lower() for c in categories):
        print("❌ La categoría ya existe")
        return

    category = Category(
        category_id=get_next_category_id(),
        name=name
    )

    categories.append(category.to_dict())
    save_all_categories(categories)

    log_action(
        user=current_user,
        action="Creó categoría",
        reason=name
    )

    print("✅ Categoría creada correctamente")


def list_categories():
    return load_categories()
