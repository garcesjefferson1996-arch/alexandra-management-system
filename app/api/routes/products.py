from fastapi import APIRouter
from app.services.product_service import list_products

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/")
def get_products():
    products = list_products()

    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category_id": p.category_id,
            "active": p.active
        }
        for p in products
    ]
