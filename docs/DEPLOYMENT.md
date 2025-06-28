# Deployment Guide

This guide explains how to deploy your FastAPI application with proper Alembic database migration management across different environments.

## Alembic Configuration Strategy

### File Structure
```
├── alembic.ini              # Development configuration (SQLite)
├── alembic.ini.template     # Template for new environments
├── alembic.production.ini   # Production config (git-ignored)
├── alembic.staging.ini      # Staging config (git-ignored)
└── alembic/
    └── env.py              # Modified to support environment variables
```

### Environment Variable Support

The `alembic/env.py` has been modified to prioritize the `DATABASE_URL` environment variable over the configuration file. This allows for secure, environment-specific database connections.

## Deployment Scenarios

### 1. Local Development
Use the default `alembic.ini` with SQLite:
```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### 2. Staging Environment

**Setup:**
1. Copy the template: `cp alembic.ini.template alembic.staging.ini`
2. Set environment variables:
```bash
export DATABASE_URL="postgresql://user:password@staging-host:5432/staging_db"
```

**Deploy:**
```bash
# Use staging config
alembic -c alembic.staging.ini upgrade head

# Or use environment variable (recommended)
DATABASE_URL="postgresql://..." alembic upgrade head
```

### 3. Production Environment

**Setup:**
1. Copy the template: `cp alembic.ini.template alembic.production.ini`
2. Set environment variables securely (recommended approach):

```bash
export DATABASE_URL="postgresql://user:password@prod-host:5432/prod_db"
```

**Deploy:**
```bash
# Recommended: Use environment variable
DATABASE_URL="postgresql://..." alembic upgrade head

# Alternative: Use production config
alembic -c alembic.production.ini upgrade head
```

## Docker Deployment

### Dockerfile Example
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run migrations on startup
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### Docker Compose with Environment Variables
```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
    depends_on:
      - db
    ports:
      - "8000:8000"

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## CI/CD Pipeline Integration

### GitHub Actions Example
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          alembic upgrade head
          
      - name: Deploy application
        # Your deployment steps here
        run: echo "Deploy to production"
```

## Environment Variables

### Required
- `DATABASE_URL`: Complete database connection string

### Examples
```bash
# PostgreSQL
DATABASE_URL="postgresql://username:password@localhost:5432/dbname"

# PostgreSQL with SSL
DATABASE_URL="postgresql://username:password@host:5432/dbname?sslmode=require"

# MySQL
DATABASE_URL="mysql+pymysql://username:password@localhost:3306/dbname"

# SQLite (development only)
DATABASE_URL="sqlite:///./app.db"
```

## Security Best Practices

### 1. Never Commit Sensitive Configs
- Production and staging `.ini` files are git-ignored
- Use environment variables for all sensitive data

### 2. Use Secrets Management
- **Production**: Use cloud provider secrets (AWS Secrets Manager, Azure Key Vault, etc.)
- **CI/CD**: Use GitHub Secrets, GitLab CI Variables, etc.
- **Local**: Use `.env` files (also git-ignored)

### 3. Database Connection Security
- Use SSL connections in production
- Limit database user permissions
- Use connection pooling appropriately

## Migration Workflow

### Development
1. Make model changes in `app/models.py`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review and edit the generated migration file
4. Test migration: `alembic upgrade head`
5. Commit migration files to git

### Production Deployment
1. Deploy code with new migration files
2. Run migrations: `DATABASE_URL="..." alembic upgrade head`
3. Start application

### Rollback Strategy
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123

# Show migration history
alembic history
```

## Troubleshooting

### Common Issues

1. **"Can't locate revision identified by 'head'"**
   - Solution: Ensure the database has been initialized with `alembic upgrade head`

2. **Connection refused errors**
   - Check `DATABASE_URL` format
   - Verify database server is running
   - Check firewall/network connectivity

3. **Permission denied**
   - Ensure database user has necessary permissions
   - Check if database exists

### Debug Commands
```bash
# Show current revision
alembic current

# Show pending migrations
alembic heads

# Validate migration files
alembic check

# Show SQL without executing
alembic upgrade head --sql
```

## Monitoring

Consider implementing:
- Migration logging in production
- Health checks that verify database connectivity
- Alerts for failed migrations
- Backup strategies before major migrations

## Notes

- Always backup your production database before running migrations
- Test migrations on staging environment first
- Keep migration files in version control
- Document any manual migration steps
- Monitor application startup time (migrations can be slow) 