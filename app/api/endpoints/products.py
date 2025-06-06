from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.models import Product, User_Pydantic

router = APIRouter()

# Sample products data
products = [
    Product(id=1, name="Macbook Pro", price=1000, date_added="2025-01-01"),
    Product(id=2, name="iPhone 15", price=1000, date_added="2025-01-01"),
    Product(id=3, name="iPad Pro", price=1000, date_added="2025-01-01"),
    Product(id=4, name="Apple Watch", price=1000, date_added="2025-01-01"),
    Product(id=5, name="AirPods Pro", price=1000, date_added="2025-01-01"),
]

@router.get("/products")
def get_products() -> list[Product]:
    return products

@router.get("/products/{product_id}")
def get_product(product_id: int):
    return next((product for product in products if product.id == product_id), None)

@router.post("/products")
async def create_product(product: Product, user: User_Pydantic = Depends(get_current_user)):
    products.append(product)
    return product

@router.put("/products/{product_id}")
async def update_product(product_id: int, product: Product, user: User_Pydantic = Depends(get_current_user)):
    return next((product for product in products if product.id == product_id), None) 