# Configuration Management Guide

This document explains the configuration organization for the FastAPI project, including the centralized `config/` directory structure and best practices.

## Overview

All configuration files have been organized into the `config/` directory to improve project structure and deployment management. This approach provides:

- **Centralized Configuration**: All config files in one location
- **Environment Management**: Clear separation between development, staging, and production
- **Tool Compatibility**: Wrapper files maintain compatibility with standard tools
- **Security**: Clear separation of sensitive and non-sensitive configuration

## Directory Structure

```
project_root/
├── config/                    # Centralized configuration directory
│   ├── README.md              # Configuration documentation
│   ├── alembic.ini            # Main Alembic configuration
│   ├── alembic.ini.template   # Template for environment-specific configs
│   ├── pytest.ini            # Pytest testing configuration
│   ├── env.example            # Environment variables template
│   ├── docker.env.example     # Docker environment template
│   ├── app_config.py          # Centralized application configuration
│   └── logging.yaml           # Structured logging configuration
├── alembic.ini                # Wrapper (for command compatibility)
├── pytest.ini                # Wrapper (for command compatibility)
├── requirements.txt           # Python dependencies (project root)
└── .env                       # Local environment variables (git-ignored)
```

## Dependency Management

The project uses a clear dependency management structure:

### Core Dependencies (`requirements.txt`)
Contains only the essential packages needed to run the application in production:
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
Includes all core dependencies plus additional tools for development:
```bash
# Install for development (includes core + dev tools)
pip install -r requirements-dev.txt

# Install for production (core only)
pip install -r requirements.txt
```

Development dependencies include:
- Testing frameworks (pytest, pytest-cov)
- Code quality tools (black, isort, flake8, mypy)
- Development utilities (ipython, ipdb)

## Configuration Files

### Core Configuration Files

#### `config/alembic.ini`
Main Alembic configuration with detailed settings for database migrations.

**Usage:**
```bash
# Use wrapper from project root (recommended)
alembic revision --autogenerate -m "description"

# Or use directly
alembic -c config/alembic.ini revision --autogenerate -m "description"
```

#### `config/pytest.ini`
Detailed pytest configuration including test paths, coverage settings, and markers.

**Usage:**
```bash
# Use wrapper from project root (recommended)
pytest

# Or specify config directly
pytest -c config/pytest.ini
```



### Environment Configuration

#### `config/env.example`
Template for local development environment variables.

**Setup:**
```bash
# Copy template to project root
cp config/env.example .env

# Edit with your values
nano .env
```

#### `config/docker.env.example`
Template for Docker containerized deployments.

**Setup:**
```bash
# For production deployment
cp config/docker.env.example .env.production

# Edit with production values
nano .env.production
```

### Application Configuration

#### `config/app_config.py`
Centralized application configuration using Pydantic Settings.

**Features:**
- Environment-specific settings (development, production, testing)
- Validation of configuration values
- Type hints for all settings
- Automatic environment variable loading

**Usage:**
```python
from config.app_config import settings, get_settings_by_environment

# Use default settings
app_settings = settings

# Use environment-specific settings
prod_settings = get_settings_by_environment("production")
```

### Logging Configuration

#### `config/logging.yaml`
Structured logging configuration with multiple handlers and formatters.

**Features:**
- Console and file logging
- Structured JSON logging option
- Different log levels for different components
- Automatic log rotation (when configured)

## Wrapper Files

Wrapper files in the project root maintain compatibility with standard tooling while pointing to the centralized configurations.

### `alembic.ini` (wrapper)
Minimal configuration that allows standard Alembic commands to work from the project root.

### `pytest.ini` (wrapper)
Basic pytest configuration that works with the detailed config in `config/pytest.ini`.



## Environment-Specific Configurations

### Development
Use the wrapper files and local `.env` file:
```bash
cp config/env.example .env
# Edit .env with development values
```

### Staging
Create staging-specific configurations:
```bash
python deploy_setup.py staging postgresql://user:pass@staging-host/db
```

### Production
Create production-specific configurations:
```bash
python deploy_setup.py production postgresql://user:pass@prod-host/db
```

## Configuration Best Practices

### 1. Environment Variables
- Use for sensitive data (passwords, API keys)
- Use for environment-specific settings (database URLs, debug flags)
- Never commit sensitive values to Git

### 2. Configuration Files
- Use for static configuration and defaults
- Commit non-sensitive configuration to Git
- Use templates for documentation and setup

### 3. Validation
- Use Pydantic Settings for configuration validation
- Define type hints for all configuration values
- Provide sensible defaults where appropriate

### 4. Documentation
- Document all configuration options
- Provide examples in template files
- Keep this guide updated with changes

## Migration from Old Structure

If you're migrating from the old structure where config files were in the project root:

1. **Moved Files**: The following files have been moved to `config/`:
   - `alembic.ini` → `config/alembic.ini`
   - `alembic.ini.template` → `config/alembic.ini.template`
   - `pytest.ini` → `config/pytest.ini`

2. **Wrapper Files**: New wrapper files in the project root maintain compatibility

3. **New Files**: Additional configuration files have been added:
   - `config/env.example`
   - `config/docker.env.example`
   - `config/app_config.py`
   - `config/logging.yaml`

4. **References**: Update any scripts or documentation that directly reference the old file locations

## Troubleshooting

### Tool Not Finding Configuration
If a tool can't find its configuration:
1. Make sure the wrapper file exists in the project root
2. Check if the tool supports the `-c` flag to specify config location
3. Run the tool from the project root directory

### Environment Variables Not Loading
1. Ensure `.env` file is in the project root (not in `config/`)
2. Check that the `.env` file is not in `.gitignore`
3. Verify environment variable names match those in `config/app_config.py`

### Database Connection Issues
1. Check `DATABASE_URL` in your `.env` file
2. Ensure the database service is running
3. Verify connection parameters in the environment configuration

## Security Considerations

1. **Never commit sensitive data** to configuration files
2. **Use environment variables** for all secrets
3. **Review .gitignore** to ensure sensitive files are excluded
4. **Use different secrets** for different environments
5. **Rotate secrets regularly** in production

## Contributing

When adding new configuration:
1. Add the config file to the `config/` directory
2. Create a wrapper in the project root if needed for tool compatibility
3. Update this documentation
4. Update the `.gitignore` if the config contains sensitive data
5. Provide a template or example configuration 