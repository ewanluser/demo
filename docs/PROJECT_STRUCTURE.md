# Project Structure Guide

This document explains the organizational structure of the FastAPI User Management API project.

## 📁 Project Overview

```
startup/
├── 📁 app/                      # Application source code
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   ├── models.py                # SQLAlchemy database models
│   ├── schemas.py               # Pydantic validation schemas
│   ├── crud.py                  # Database CRUD operations
│   └── database.py              # Database connection and configuration
├── 📁 config/                   # Configuration files (centralized)
│   ├── README.md                # Configuration documentation
│   ├── alembic.ini              # Detailed Alembic configuration
│   ├── alembic.ini.template     # Template for environment-specific configs
│   ├── pytest.ini              # Detailed pytest configuration
│   ├── env.example              # Environment variables template
│   ├── docker.env.example       # Docker environment template
│   ├── app_config.py            # Application configuration (Pydantic)
│   └── logging.yaml             # Structured logging configuration
├── 📁 alembic/                  # Database migrations
│   ├── env.py                   # Alembic environment configuration
│   ├── script.py.mako           # Migration script template
│   └── versions/                # Generated migration files
├── 📁 tests/                    # Test suite
│   ├── conftest.py              # Test configuration and fixtures
│   ├── test_*.py                # Test files
│   └── requirements.txt         # Test-specific dependencies
├── 📁 docs/                     # Documentation
│   ├── README.md                # Main project documentation
│   ├── CONFIGURATION.md         # Configuration guide
│   ├── PROJECT_SUMMARY.md       # Technical overview
│   └── TESTING.md               # Testing documentation
├── 📁 .cursor/                  # Cursor IDE configuration
│   └── rules/                   # Modern cursor rules (*.mdc files)
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── alembic.ini                  # Alembic wrapper (command compatibility)
├── pytest.ini                  # Pytest wrapper (command compatibility)
├── run_dev.py                   # Development server runner
├── run_tests.py                 # Test runner with options
└── deploy_setup.py              # Deployment configuration helper
```

## 🎯 Design Principles

### 1. **Separation of Concerns**
- **Application Logic** (`app/`) - Core business logic and API
- **Configuration** (`config/`) - All configuration files centralized  
- **Tests** (`tests/`) - Comprehensive test suite with fixtures
- **Documentation** (`docs/`) - Project documentation and guides
- **Database** (`alembic/`) - Migration scripts and database management

### 2. **Environment Management**
- **Development**: Use `requirements-dev.txt` and `.env` file
- **Production**: Use `requirements.txt` and environment variables
- **Testing**: Isolated database and test-specific configuration

### 3. **Tool Compatibility**
- **Wrapper Files**: Maintain compatibility with standard commands
- **Centralized Config**: Detailed configuration in `config/` directory
- **Environment Variables**: Runtime configuration via `.env` files

## 📦 Dependency Management

### Production Dependencies (`requirements.txt`)
**Purpose**: Minimal dependencies needed to run the application in production.

```
fastapi
uvicorn[standard]
sqlalchemy
alembic
psycopg2-binary
python-multipart
email-validator
requests
```

### Development Dependencies (`requirements-dev.txt`)
**Purpose**: All production dependencies plus development tools.

**Includes**:
- Core production dependencies (via `-r requirements.txt`)
- Testing frameworks (pytest, pytest-cov, pytest-asyncio)
- Code quality tools (black, isort, flake8, mypy)
- Development utilities (ipython, ipdb)

**Usage**:
```bash
# Development environment
pip install -r requirements-dev.txt

# Production environment  
pip install -r requirements.txt
```

## ⚙️ Configuration Management

### Configuration Hierarchy
1. **Wrapper Files** (project root) - Command compatibility
2. **Detailed Config** (`config/`) - Centralized configuration
3. **Environment Variables** (`.env`) - Runtime settings
4. **Environment-Specific** (`alembic.{env}.ini`) - Deployment configs

### Configuration Categories

#### **Application Configuration**
- `config/app_config.py` - Centralized Pydantic settings
- `config/env.example` - Environment variables template
- `config/docker.env.example` - Docker deployment template

#### **Tool Configuration**
- `config/alembic.ini` - Database migration configuration
- `config/pytest.ini` - Testing framework configuration
- `config/logging.yaml` - Structured logging setup

#### **Wrapper Files**
- `alembic.ini` - Allows `alembic` commands from project root
- `pytest.ini` - Allows `pytest` commands from project root

## 🧪 Testing Structure

### Test Organization
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints with database
- **Fixtures**: Reusable test data and configuration
- **Coverage**: Comprehensive test coverage reporting

### Test Configuration
- `tests/conftest.py` - Test fixtures and configuration
- `config/pytest.ini` - Detailed pytest settings
- `pytest.ini` - Wrapper for command compatibility

## 📚 Documentation Strategy

### Documentation Types
- **User Documentation**: Setup, usage, and API guides
- **Developer Documentation**: Architecture, testing, and contribution guides
- **Configuration Documentation**: Environment setup and deployment
- **API Documentation**: Automatic OpenAPI/Swagger generation

### Documentation Structure
- `docs/README.md` - Main project documentation
- `docs/CONFIGURATION.md` - Configuration management guide
- `docs/PROJECT_SUMMARY.md` - Technical overview
- `docs/TESTING.md` - Testing guidelines

## 🚀 Development Workflow

### Local Development
1. **Setup**: `pip install -r requirements-dev.txt`
2. **Database**: `alembic upgrade head`
3. **Development**: `python run_dev.py`
4. **Testing**: `python run_tests.py`

### Configuration Setup
1. **Environment**: `cp config/env.example .env`
2. **Customize**: Edit `.env` with your settings
3. **Database**: Configure `DATABASE_URL` in `.env`

### Adding Features
1. **Models**: Add to `app/models.py`
2. **Schemas**: Add to `app/schemas.py`
3. **CRUD**: Add to `app/crud.py`
4. **API**: Add to `app/main.py`
5. **Tests**: Add to `tests/test_*.py`
6. **Migration**: `alembic revision --autogenerate -m "description"`

## 🔒 Security Considerations

### Configuration Security
- **No Secrets in Git**: Never commit sensitive data
- **Environment Variables**: Use for all secrets and API keys
- **Template Files**: Provide examples without real credentials
- **Production Configs**: Generate on deployment server

### Best Practices
- Use different secrets for different environments
- Rotate secrets regularly
- Review `.gitignore` for sensitive file exclusion
- Validate configuration with Pydantic

## 📈 Scalability

### Project Growth
- **Feature Modules**: Organize into `app/features/` subdirectories
- **Service Layer**: Add `app/services/` for business logic
- **API Versioning**: Use `app/api/v1/`, `app/api/v2/` structure
- **Microservices**: Split into separate FastAPI applications

### Configuration Scaling
- **Environment-Specific**: Multiple config files per environment
- **Service Discovery**: External configuration management
- **Secret Management**: Dedicated secret management services
- **Feature Flags**: Configuration-driven feature toggles

## 🤝 Contributing

When adding to the project:
1. **Follow Structure**: Place files in appropriate directories
2. **Update Documentation**: Keep docs current with changes
3. **Test Coverage**: Add tests for new functionality
4. **Configuration**: Add config options to appropriate files
5. **Dependencies**: Update `requirements-dev.txt` for dev tools

---

This structure supports both rapid development and production deployment while maintaining code quality and clear organization. 