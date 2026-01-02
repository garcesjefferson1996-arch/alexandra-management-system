from app.models.expense import Expense
from app.repositories.expense_repo import save_expense
from app.services.audit_service import log_action

EXPENSE_CATEGORIES = [
    "Insumos",
    "Servicios básicos",
    "Mantenimiento",
    "Sueldos",
    "Transporte",
    "Otros"
]


def register_expense(current_user):
    print("\n📉 REGISTRAR GASTO")

    try:
        amount = float(input("Monto del gasto: $"))
    except ValueError:
        print("❌ Monto inválido")
        return

    print("\nCategoría:")
    for i, category in enumerate(EXPENSE_CATEGORIES, start=1):
        print(f"{i}. {category}")

    try:
        category_index = int(input("Seleccione categoría: ")) - 1
        category = EXPENSE_CATEGORIES[category_index]
    except (ValueError, IndexError):
        print("❌ Categoría inválida")
        return

    description = input("Descripción: ")

    expense = Expense(
        amount=amount,
        category=category,
        description=description,
        user=current_user.username
    )

    save_expense(expense.to_dict())

    log_action(
    user=current_user,
    action="Registró un gasto",
    reason=f"{category} | ${amount:.2f} | {description}"
)

    print("✅ Gasto registrado correctamente")
