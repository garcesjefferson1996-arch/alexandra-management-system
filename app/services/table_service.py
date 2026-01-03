from app.models.table import Table
from app.repositories.table_repo import (
    load_tables,
    save_tables,
    get_next_table_id
)

# =========================
# LISTAR MESAS
# =========================

def list_tables():
    return load_tables()


def list_free_tables():
    """
    Retorna solo mesas libres
    """
    tables = load_tables()
    return [t for t in tables if t["status"] == "FREE"]


# =========================
# CREAR MESA (ADMIN)
# =========================

def create_table(name: str):
    tables = load_tables()

    table = Table(
        table_id=get_next_table_id(),
        name=name
    )

    tables.append(table.to_dict())
    save_tables(tables)

    return table


# =========================
# CAMBIAR ESTADO
# =========================

def occupy_table(table_id: int):
    tables = load_tables()

    for table in tables:
        if table["table_id"] == table_id:
            table["status"] = "OCCUPIED"
            save_tables(tables)
            return True

    return False


def free_table(table_id: int):
    tables = load_tables()

    for table in tables:
        if table["table_id"] == table_id:
            table["status"] = "FREE"
            save_tables(tables)
            return True

    return False
