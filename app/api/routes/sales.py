from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.models.sale import Sale
from app.services.sale_service import register_sale
from app.services.product_service import list_products
from app.repositories.sale_repo import get_next_sale_id
from app.models.user import User

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

# ---------- SCHEMAS (lo que recibe la API) ----------

class SaleItemRequest(BaseModel):
    product_id: int
    quantity: int = 1


class SaleRequest(BaseModel):
    items: List[SaleItemRequest]
    user: str = "api"  # quién registra la venta


# ---------- ENDPOINT ----------

@router.post("/")
def create_sale_api(payload: SaleRequest):
    products = list_products()
    products_map = {p.id: p for p in products}

    if not payload.items:
        raise HTTPException(status_code=400, detail="La venta no tiene productos")

    sale = Sale(get_next_sale_id())

    for item in payload.items:
        product = products_map.get(item.product_id)

        if not product or not product.active:
            raise HTTPException(
                status_code=404,
                detail=f"Producto inválido o inactivo (ID {item.product_id})"
            )

        for _ in range(item.quantity):
            sale.add_product(product)

    fake_user = User(payload.user, "api", "admin")
    register_sale(sale, fake_user)

    return {
        "sale_id": sale.sale_id,
        "total": sale.total,
        "items": sale.items,
        "timestamp": sale.timestamp
    }
