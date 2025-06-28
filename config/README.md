# Configuration Directory

This directory contains configuration files for the FastAPI project. Note that dependency files (`requirements.txt`, `requirements-dev.txt`) remain in the project root as they are dependency manifests, not configuration files.

## Configuration Files

### Core Configuration

- **`alembic.ini`** - Main Alembic configuration for database migrations
- **`alembic.ini.template`** - Template for environment-specific Alembic configurations
- **`pytest.ini`** - Pytest testing configuration

### Environment Configuration

- **`env.example`** - Environment variables template (copy to `.env` in project root)
- **`docker.env.example`** - Docker environment variables template
- **`app_config.py`** - Centralized application configuration using Pydantic

### Logging Configuration

- **`logging.yaml`** - Structured logging configuration

## Usage

### Development

For development, use the wrapper files in the project root:
- `alembic.ini` (wrapper) → points to `config/alembic.ini`
- `pytest.ini` (wrapper) → includes config from `config/pytest.ini`

### Environment Setup

1. Copy environment template:
   ```bash
   cp config/env.example .env
   ```

2. Edit `.env` with your specific values

3. For Docker deployment:
   ```bash
   cp config/docker.env.example .env.production
   ```

### Database Migrations

Run Alembic commands from the project root as usual:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

The wrapper `alembic.ini` will automatically use the configuration from `config/alembic.ini`.

### Testing

Run tests from the project root:
```bash
pytest
# or
python run_tests.py
```

The wrapper `pytest.ini` will use the configuration from `config/pytest.ini`.

## Environment-Specific Configurations

### Production Deployment

Use the deployment script to create environment-specific configurations:
```bash
python deploy_setup.py production postgresql://user:pass@host/db
```

This creates `alembic.production.ini` in the project root.

### Configuration Hierarchy

1. **Wrapper files** (project root) - for command compatibility
2. **Main config** (`config/`) - detailed configuration
3. **Environment variables** (`.env`) - runtime configuration
4. **Environment-specific** (`alembic.{env}.ini`) - deployment configuration

## Configuration Management Best Practices

1. **Environment Variables**: Use for sensitive data and environment-specific settings
2. **Config Files**: Use for static configuration and defaults
3. **Templates**: Provide examples and documentation for required settings
4. **Wrappers**: Maintain compatibility with standard tooling
5. **Documentation**: Keep this README updated with configuration changes

## File References

When referencing configuration files in code or scripts:
- Use `config/filename` for internal references
- Use environment variables for runtime configuration
- Use wrapper files for command-line tools

## Security Notes

- Never commit sensitive data to configuration files
- Use environment variables for secrets
- Keep production configurations separate and secure
- Review `.gitignore` to ensure sensitive files are excluded 