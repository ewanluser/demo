# FastAPI User Management API

A high-concurrency API built with FastAPI, SQLAlchemy, and Alembic for robust user management with comprehensive testing infrastructure.

## 🚀 Quick Start

```bash
# Install development dependencies (includes all tools and testing)
pip install -r requirements-dev.txt

# Run database migrations
alembic upgrade head

# Start development server
python run_dev.py
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## ✨ Features

- **High-Concurrency API** with FastAPI's async/await support
- **Complete User Management** (CRUD operations, authentication)
- **Database Management** with SQLAlchemy ORM and Alembic migrations
- **Comprehensive Testing** with 96% code coverage (56 tests)
- **Production Ready** with proper error handling and validation
- **API Documentation** with automatic OpenAPI/Swagger generation

## 🏗️ Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping (ORM) library
- **Alembic** - Database migration tool for SQLAlchemy
- **Pydantic** - Data validation using Python type annotations
- **pytest** - Testing framework with comprehensive test suite
- **SQLite/PostgreSQL** - Database support (SQLite for dev, PostgreSQL for production)

## 📚 Documentation

- **[Project Overview](docs/README.md)** - Detailed project documentation
- **[API Guide](docs/EXAMPLE.md)** - Complete implementation guide and examples
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Technical overview and features
- **[Testing Guide](docs/TESTING.md)** - Comprehensive testing documentation
- **[Testing Summary](docs/TESTING_SUMMARY.md)** - Test infrastructure and coverage details

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage

# Run specific test categories
python run_tests.py --api      # API endpoint tests
python run_tests.py --unit     # Unit tests
python run_tests.py --integration  # Integration tests
```

**Current Status**: ✅ All 56 tests passing with 96% code coverage

## 🔧 Development

```bash
# Install all development dependencies
pip install -r requirements-dev.txt

# Run development server with auto-reload
python run_dev.py

# Create new database migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 📖 API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /users/` - Create new user
- `GET /users/` - List users (with pagination)
- `GET /users/{id}` - Get user by ID
- `GET /users/email/{email}` - Get user by email
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user
- `POST /auth/login` - User authentication

## 🚀 Deployment

For production deployment:

```bash
# Install only production dependencies
pip install -r requirements.txt
```

1. **Dependencies**: Use `requirements.txt` for production (minimal dependencies)
2. **Database**: Switch to PostgreSQL by updating `DATABASE_URL` environment variable
3. **Security**: Implement JWT authentication middleware
4. **Monitoring**: Add logging and monitoring tools
5. **Performance**: Configure connection pooling and caching
6. **Scaling**: Deploy with Docker and load balancing

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

**Built with ❤️ using FastAPI, SQLAlchemy, and modern Python practices.** 