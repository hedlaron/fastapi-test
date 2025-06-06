# FastAPI Test Project

This is a simple FastAPI project that demonstrates a basic API setup with authentication and database integration.

## Features
- REST API endpoints for products
- User authentication with OAuth2
- SQLite database with Tortoise ORM
- Token-based authentication

## Setup

1. Create a virtual environment using `uv` (recommended):
```bash
uv venv
# source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
uv add fastapi
uv add tortoise-orm
uv sync
```

## Running the Application

To run the application, use the following command:

```bash
uv run fastapi dev main.py
```

## API Endpoints

The API will be available at:
- http://127.0.0.1:8000 - Root endpoint (requires authentication)
- http://127.0.0.1:8000/token - Get authentication token
- http://127.0.0.1:8000/products - Products CRUD endpoints
- http://127.0.0.1:8000/docs - Swagger UI documentation (provided by FastAPI)
- http://127.0.0.1:8000/redoc - ReDoc documentation (provided by FastAPI)

## Database

The application uses SQLite with Tortoise ORM. The database file `db.sqlite3` will be automatically created when you first run the application.

## Project Structure

- `main.py` - Main application file containing:
  - FastAPI routes
  - Database models (User, Product)
  - Authentication logic
  - API endpoints
