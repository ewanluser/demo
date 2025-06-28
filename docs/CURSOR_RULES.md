# Cursor Rules Documentation

## Overview

This project uses the modern Cursor IDE rules format with organized `.cursor/rules/*.mdc` files instead of a single `.cursorrules` file. This provides better organization, maintainability, and focused guidelines.

## Rule Files Structure

The rules are organized into focused files in the `.cursor/rules/` directory:

### 📋 `01-project-overview.mdc`
- Project architecture overview
- FastAPI patterns and conventions
- Database patterns with SQLAlchemy
- Pydantic schema guidelines

### 🎨 `02-code-style.mdc`
- Python style guidelines (PEP 8, Black, type hints)
- Import organization standards
- File naming conventions
- Documentation standards (docstrings, API docs)

### 📁 `03-file-paths.mdc`
- Comprehensive file creation path guidelines
- Main application structure (`app/` directory)
- Feature-based organization for larger apps
- Testing, documentation, and configuration structures
- File creation rules by type (models, endpoints, schemas, CRUD)

### 🗄️ `04-database.mdc`
- Alembic migration best practices
- Model conventions and table naming
- Database session management
- Environment configuration
- Query performance optimization

### 🌐 `05-api-design.mdc`
- RESTful endpoint conventions
- Response model patterns
- Request validation with Pydantic
- Error handling strategies
- Async operation patterns

### 🧪 `06-testing.mdc`
- Test structure and naming conventions
- Pytest fixtures and test data
- Test categories (unit, integration, functional)
- Test organization and best practices

### 🔒 `07-security.mdc`
- Password hashing and authentication
- Input validation and sanitization
- Environment variable security
- API security best practices
- Database security guidelines
- Dependency security management

### 🔄 `08-workflow.mdc`
- Git conventions and branch strategy
- Code review guidelines
- Pre-commit checklist
- Pull request and issue management
- Release and hotfix processes

### 🚀 `09-deployment.mdc`
- Environment setup and variables
- Migration strategies
- Docker deployment patterns
- Health checks and monitoring
- Security considerations
- Backup and performance monitoring

### ⚡ `10-performance.mdc`
- Database performance optimization
- API performance patterns
- Memory management strategies
- Caching implementations
- Monitoring and profiling
- Best practices for scalability

## Benefits of This Structure

### 🎯 **Focused Guidelines**
- Each file covers a specific aspect of development
- Easier to find relevant rules
- Reduced cognitive load when working on specific features

### 🔍 **Better Maintainability**
- Easy to update specific areas without affecting others
- Clear separation of concerns
- Version control friendly (smaller, focused changes)

### 👥 **Team Collaboration**
- Different team members can work on different rule files
- Easier to review changes to specific guidelines
- Better onboarding with focused rule sections

### 📈 **Scalability**
- Easy to add new rule files for new features
- Can be organized by team or feature area
- Supports growing project complexity

## Usage

Cursor IDE automatically detects and uses all `.mdc` files in the `.cursor/rules/` directory. The rules are applied contextually based on:

- File type being edited
- Current development task
- Project structure and patterns

## Migration Notes

This project has migrated from the legacy `.cursorrules` format to the modern `.cursor/rules/*.mdc` format for better organization and maintainability.

### What Changed:
- ✅ Single `.cursorrules` file split into 10 focused `.mdc` files
- ✅ Better organization by functional area
- ✅ Easier maintenance and updates
- ✅ Improved team collaboration on guidelines

### File Organization:
```
.cursor/
└── rules/
    ├── 01-project-overview.mdc    # Architecture & patterns
    ├── 02-code-style.mdc          # Style & formatting
    ├── 03-file-paths.mdc          # File organization
    ├── 04-database.mdc            # Database guidelines
    ├── 05-api-design.mdc          # API patterns
    ├── 06-testing.mdc             # Testing strategies
    ├── 07-security.mdc            # Security practices
    ├── 08-workflow.mdc            # Development workflow
    ├── 09-deployment.mdc          # Deployment guidelines
    └── 10-performance.mdc         # Performance optimization
```

## Contributing to Rules

When updating rules:

1. **Find the appropriate file** for your guideline
2. **Follow the existing structure** within that file
3. **Include code examples** where helpful
4. **Update this documentation** if adding new files
5. **Test the rules** with real development scenarios

## Best Practices

- Keep rules specific and actionable
- Include code examples for clarity
- Update rules based on team feedback
- Review rules regularly for relevance
- Document any project-specific exceptions 