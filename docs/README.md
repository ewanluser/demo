# FastAPI User Management API

A high-concurrency API built with FastAPI, SQLAlchemy, and Alembic for stable data management.

## Features

- **High Performance**: Built with FastAPI for excellent async performance
- **Type Safety**: Full Pydantic validation for request/response data
- **Database Management**: SQLAlchemy ORM with Alembic migrations
- **Auto Documentation**: Interactive API docs with Swagger UI
- **User Management**: Complete CRUD operations for users
- **Authentication**: Basic login functionality
- **Data Validation**: Email validation and proper error handling

## Project Structure

```
├── app/                    # Main application package
│   ├── __init__.py        # Package initialization
│   ├── main.py            # FastAPI app and route definitions
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic models for validation
│   ├── crud.py            # Database operations (CRUD)
│   └── database.py        # Database configuration
├── tests/                 # Test suite
│   ├── __init__.py        # Test package initialization
│   ├── conftest.py        # Pytest configuration and fixtures
│   ├── test_api_endpoints.py      # API endpoint tests
│   ├── test_crud_operations.py    # CRUD operation tests
│   ├── test_models.py             # Database model tests
│   ├── test_schemas.py            # Schema validation tests
│   ├── test_integration.py        # Integration tests
│   ├── test_api_basic.py          # Basic API test script
│   ├── test_api_comprehensive.py  # Comprehensive test suite
│   ├── requirements.txt           # Test dependencies
│   └── README.md                  # Test documentation
├── alembic/               # Database migration scripts
├── alembic.ini           # Alembic configuration
├── pytest.ini           # Pytest configuration
├── run_tests.py         # Test runner script
├── requirements.txt     # Python dependencies
├── EXAMPLE.md          # Detailed implementation guide
└── README.md           # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations

```bash
# Create your first migration
alembic revision --autogenerate -m "Create users table"

# Apply migrations to database
alembic upgrade head
```

### 3. Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint (health check)
- `GET /health` - Health check endpoint

### User Management

- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination)
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `GET /users/email/{email}` - Get user by email

### Authentication

- `POST /auth/login` - Login with email and password

## Example Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "secretpassword"
     }'
```

### Get All Users

```bash
curl "http://localhost:8000/users/?skip=0&limit=10"
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "secretpassword"
     }'
```

## Database Configuration

By default, the application uses SQLite for development. To use PostgreSQL:

1. Update the `SQLALCHEMY_DATABASE_URL` in `app/database.py`:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
   ```

2. Update `alembic.ini`:
   ```ini
   sqlalchemy.url = postgresql://user:password@localhost/dbname
   ```

## Environment Variables

You can use environment variables to configure the database:

```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

## Development

### Testing

The project includes comprehensive test coverage organized in the `tests/` directory:

#### Test Structure

- **`tests/`** - Dedicated test directory with organized test suites
  - **`conftest.py`** - Pytest configuration and shared fixtures
  - **`test_api_endpoints.py`** - API endpoint tests
  - **`test_crud_operations.py`** - Database CRUD operation tests
  - **`test_models.py`** - Database model tests
  - **`test_schemas.py`** - Pydantic schema validation tests
  - **`test_integration.py`** - Integration workflow tests
  - **`test_api_basic.py`** - Basic API test script
  - **`test_api_comprehensive.py`** - Comprehensive test suite

#### Running Tests

**Using the Test Runner (Recommended):**
```bash
# Quick smoke test
python run_tests.py --quick

# Run all tests
python run_tests.py --all

# Run specific test categories
python run_tests.py --unit          # Unit tests (models, schemas, CRUD)
python run_tests.py --api           # API endpoint tests
python run_tests.py --integration   # Integration tests

# Run with coverage report
python run_tests.py --coverage

# Get help
python run_tests.py --help
```

**Using pytest directly:**
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/

# Run specific test files
pytest tests/test_api_endpoints.py -v
pytest tests/test_crud_operations.py -v

# Run specific test classes
pytest tests/test_api_endpoints.py::TestUserEndpoints -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html
```

**Legacy test scripts:**
```bash
# Basic API tests
python tests/test_api_basic.py

# Comprehensive test suite
python tests/test_api_comprehensive.py
```

### Adding New Features

1. Add new models in `app/models.py`
2. Create corresponding Pydantic schemas in `app/schemas.py`
3. Implement CRUD operations in `app/crud.py`
4. Add API endpoints in `app/main.py`
5. Create and run migrations:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   alembic upgrade head
   ```

## Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Gunicorn

For production, use Gunicorn with Uvicorn workers:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Security Notes

⚠️ **Important**: This example uses simple password hashing for demonstration. In production:

1. Use proper password hashing (bcrypt, argon2)
2. Implement JWT tokens for authentication
3. Add rate limiting
4. Use HTTPS
5. Validate and sanitize all inputs
6. Implement proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational purposes. Feel free to use and modify as needed. 