# FastAPI Test Project

This is a simple FastAPI project that demonstrates a basic API setup with authentication and database integration.

## Features
- REST API endpoints for products
- JWT-based authentication
- User registration and login
- SQLite database with Tortoise ORM
- Token-based protected endpoints

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
uv add passlib
uv add pyjwt
uv sync
```

## Running the Application

To run the application, use the following command:

```bash
uv run fastapi dev main.py
```

## API Endpoints

### Authentication
- `POST /users` - Register a new user
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- `POST /token` - Login and get access token
  ```bash
  # Using form data
  username=your_username&password=your_password
  ```

### User Operations
- `GET /users/me` - Get current user info (requires authentication)
- `GET /` - Test authentication (requires authentication)

### Products
- `GET /products` - List all products
- `GET /products/{product_id}` - Get a specific product
- `POST /products` - Create a new product (requires authentication)
  ```json
  {
    "id": 1,
    "name": "Product Name",
    "price": 99.99,
    "date_added": "2024-01-01"
  }
  ```
- `PUT /products/{product_id}` - Update a product (requires authentication)

## Authentication

To access protected endpoints:
1. First, create a user using the `/users` endpoint
2. Get a token using the `/token` endpoint
3. Include the token in subsequent requests:
   ```
   Authorization: Bearer your_token_here
   ```

## Database

The application uses SQLite with Tortoise ORM. The database file `db.sqlite3` will be automatically created when you first run the application.

## Project Structure

- `main.py` - Main application file containing:
  - FastAPI routes
  - Database models (User, Product)
  - Authentication logic
  - API endpoints
  - JWT token handling
