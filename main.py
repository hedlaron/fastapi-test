from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import fields, models
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from passlib.hash import bcrypt
import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = "itsnotasecretanymore"

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    @classmethod
    async def get_user(cls, username: str):
        return await cls.get(username=username)
    
    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password_hash)

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create Pydantic models for request/response
class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int 
    username: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return await User_Pydantic.from_tortoise_orm(user)

@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password))
    await user_obj.save()
    return {"id": user_obj.id, "username": user_obj.username}

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

async def authenticate_user(username: str, password: str):
    try:
        user = await User.get_user(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.verify_password(password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.model_dump(), JWT_SECRET)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
async def index(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.get("/users/me")
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user

@app.get("/products")
def get_products() -> list[Product]:
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return next((product for product in products if product["id"] == product_id), None)

@app.post("/products")
async def create_product(product: Product, user: User_Pydantic = Depends(get_current_user)):
    products.append(product)
    return product

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product, user: User_Pydantic = Depends(get_current_user)):
    return next((product for product in products if product["id"] == product_id), None)

# Register Tortoise ORM
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)