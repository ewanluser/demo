from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Create a Base class that our ORM models will inherit from
class Base(DeclarativeBase):
    pass

# Database connection URL
# You can change this to your preferred database
# For development, we'll use SQLite for simplicity
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./fastapi_app.db"
)

# For PostgreSQL, use this format instead:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/fastapi_db"

# Create the database engine
# For SQLite, we need to add connect_args
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    """
    Database dependency that provides a database session.
    This function is used by FastAPI's dependency injection system.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 