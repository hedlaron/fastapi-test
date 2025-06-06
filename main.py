from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import fields, models
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password = fields.CharField(255)

    @classmethod
    async def get_user(cls, username: str):
        return await cls.get(username=username)
    

    def verify_password(self, password: str):
        return True

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

class Product(BaseModel):
    id: int
    name: str
    price: float
    date_added: str

products = [
    Product(id=1, name="Macbook Pro", price=1000, date_added="2025-01-01"),
    Product(id=2, name="iPhone 15", price=1000, date_added="2025-01-01"),
    Product(id=3, name="iPad Pro", price=1000, date_added="2025-01-01"),
    Product(id=4, name="Apple Watch", price=1000, date_added="2025-01-01"),
    Product(id=5, name="AirPods Pro", price=1000, date_added="2025-01-01"),
]

@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/")
async def index(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/products")
def get_products() -> list[Product]:
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return next((product for product in products if product["id"] == product_id), None)

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    return next((product for product in products if product["id"] == product_id), None)

# Register Tortoise ORM
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)