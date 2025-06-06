from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Test API"
    jwt_secret: str = "itsnotasecretanymore"
    database_url: str = "sqlite://db.sqlite3"

settings = Settings() 