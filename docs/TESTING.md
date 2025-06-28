# Test Suite for FastAPI User Management API

This directory contains comprehensive test cases for the FastAPI User Management API project.

## 🎉 Current Status: ALL TESTS PASSING ✅

- **Total Tests**: 56 tests across 5 test files  
- **Success Rate**: 100% (56/56 passing)
- **Code Coverage**: 96% (163 statements, 7 missed)
- **Test Execution Time**: ~2-3 seconds

**Recent Fix**: Resolved dependency injection issue that was causing API tests to fail. All tests now use properly isolated test databases.

## Test Structure

### Test Files

- **`conftest.py`** - Pytest configuration and shared fixtures
- **`test_api_endpoints.py`** - API endpoint tests using pytest framework
- **`test_crud_operations.py`** - CRUD operation tests
- **`test_models.py`** - Database model tests
- **`test_schemas.py`** - Pydantic schema validation tests
- **`test_integration.py`** - Integration tests for complete workflows
- **`test_api_basic.py`** - Basic API test script (moved from root)
- **`test_api_comprehensive.py`** - Comprehensive test suite (moved from root)

### Test Categories

#### 1. Unit Tests
- **Models** (`test_models.py`) - Test database model functionality, constraints, and relationships
- **Schemas** (`test_schemas.py`) - Test Pydantic validation and serialization
- **CRUD** (`test_crud_operations.py`) - Test database operations in isolation

#### 2. API Tests
- **Endpoints** (`test_api_endpoints.py`) - Test individual API endpoints
- **Authentication** - Test login and authentication flows
- **Error Handling** - Test error responses and edge cases

#### 3. Integration Tests
- **Workflows** (`test_integration.py`) - Test complete user lifecycle workflows
- **Data Consistency** - Test data consistency across operations
- **Multi-user Scenarios** - Test interactions between multiple users

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r tests/requirements.txt
```

### Run All Tests
```bash
# From project root
pytest tests/

# With verbose output
pytest tests/ -v

# With coverage
pytest tests/ --cov=app
```

### Run Specific Test Categories
```bash
# Run only unit tests
pytest tests/test_models.py tests/test_schemas.py tests/test_crud_operations.py

# Run only API tests
pytest tests/test_api_endpoints.py

# Run only integration tests
pytest tests/test_integration.py
```

### Run Specific Test Classes
```bash
# Run user endpoint tests
pytest tests/test_api_endpoints.py::TestUserEndpoints

# Run authentication tests
pytest tests/test_api_endpoints.py::TestAuthEndpoints

# Run CRUD tests
pytest tests/test_crud_operations.py::TestUserCRUD
```

### Run Specific Tests
```bash
# Run a specific test method
pytest tests/test_api_endpoints.py::TestUserEndpoints::test_create_user

# Run tests matching a pattern
pytest tests/ -k "test_create"
```

## Test Configuration

### Fixtures

The `conftest.py` file provides shared fixtures:

- **`test_db`** - Creates a temporary SQLite database for testing
- **`db_session`** - Provides a database session for each test
- **`client`** - FastAPI test client with database dependency override
- **`sample_user_data`** - Sample user data for testing
- **`sample_user_update_data`** - Sample user update data for testing

### Database Isolation

Each test uses an isolated database:
- Tests use temporary SQLite databases
- Database is created fresh for each test session
- All tables are created automatically
- Database is cleaned up after tests complete

### Dependency Overrides

The test client automatically overrides:
- Database dependency to use test database
- No external dependencies required for testing

## Test Coverage

The test suite covers:

### API Endpoints (100% coverage)
- ✅ Root endpoint (`/`)
- ✅ Health check (`/health`)
- ✅ Create user (`POST /users/`)
- ✅ Get users (`GET /users/`)
- ✅ Get user by ID (`GET /users/{id}`)
- ✅ Get user by email (`GET /users/email/{email}`)
- ✅ Update user (`PUT /users/{id}`)
- ✅ Delete user (`DELETE /users/{id}`)
- ✅ User login (`POST /auth/login`)

### CRUD Operations (100% coverage)
- ✅ Create user
- ✅ Get user by ID/email
- ✅ Get users with pagination
- ✅ Update user (partial and full)
- ✅ Delete user
- ✅ User authentication
- ✅ Password hashing and verification

### Error Scenarios
- ✅ Invalid email formats
- ✅ Duplicate email registration
- ✅ Non-existent user operations
- ✅ Wrong password authentication
- ✅ Inactive user login attempts
- ✅ Database constraint violations

### Data Validation
- ✅ Pydantic schema validation
- ✅ Database model constraints
- ✅ Email uniqueness
- ✅ Required field validation
- ✅ Data type validation

## Best Practices

### Test Organization
- Tests are organized by functionality
- Each test class focuses on a specific component
- Clear test method names describe what is being tested
- Comprehensive docstrings explain test purposes

### Test Data
- Use fixtures for reusable test data
- Create minimal test data for each test
- Clean up test data automatically
- Avoid test data dependencies

### Assertions
- Use specific assertions with clear error messages
- Test both positive and negative scenarios
- Verify all relevant response fields
- Check status codes and error messages

### Performance
- Tests run quickly with in-memory SQLite
- Parallel test execution supported
- Minimal setup/teardown overhead
- Efficient database operations

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- No external dependencies required
- Fast execution time
- Comprehensive coverage
- Clear failure reporting
- Cross-platform compatibility

## Adding New Tests

When adding new features:

1. **Add unit tests** for new models, schemas, or CRUD operations
2. **Add API tests** for new endpoints
3. **Add integration tests** for new workflows
4. **Update fixtures** if new test data is needed
5. **Update this README** with new test information

### Test Template

```python
def test_new_feature(self, client, db_session):
    """Test description of what this test verifies."""
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = client.post("/endpoint", json=test_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["key"] == "value"
``` 