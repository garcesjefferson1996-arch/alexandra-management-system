from fastapi import FastAPI
from app.api.routes.products import router as products_router
from app.api.routes.sales import router as sales_router

app = FastAPI(
    title="The Alexandra POS API",
    version="1.0.0"
)

app.include_router(products_router)
app.include_router(sales_router)

@app.get("/")
def root():
    return {"message": "The Alexandra POS API is running"}
