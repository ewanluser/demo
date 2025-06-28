"""
Pytest configuration and shared fixtures for FastAPI User Management API tests.
"""

import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app import models


@pytest.fixture(scope="session")
def test_db():
    """Create a temporary test database."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    # Create test engine
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal, engine
    
    # Cleanup - close all connections first
    engine.dispose()
    
    # Then cleanup files
    try:
        os.close(db_fd)
        os.unlink(db_path)
    except (OSError, PermissionError):
        # If we can't delete the temp file, it's not critical for tests
        pass


@pytest.fixture(scope="function")
def db_session(test_db):
    """Create a database session for each test."""
    TestingSessionLocal, engine = test_db
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        # Clean up - remove all data from tables
        session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up dependency override
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def sample_user_update_data():
    """Sample user update data for testing."""
    return {
        "email": "updated@example.com",
        "is_active": False
    } 