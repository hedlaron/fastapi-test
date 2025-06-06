from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings
from app.api.endpoints import auth, products

app = FastAPI(title=settings.app_name)

# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(products.router, tags=["products"])

# Register Tortoise ORM
register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["app.db.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
) 