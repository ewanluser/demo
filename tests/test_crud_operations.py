"""
Test cases for CRUD operations.
"""

import pytest
from app import crud, schemas, models


class TestUserCRUD:
    """Test user CRUD operations."""
    
    def test_create_user(self, db_session):
        """Test creating a user."""
        user_data = schemas.UserCreate(email="test@example.com", password="testpassword")
        user = crud.create_user(db_session, user_data)
        
        assert user.email == "test@example.com"
        assert user.hashed_password != "testpassword"  # Should be hashed
        assert user.is_active is True
        assert user.id is not None
        assert user.created_at is not None
    
    def test_get_user_by_id(self, db_session):
        """Test getting a user by ID."""
        # Create a user
        user_data = schemas.UserCreate(email="test@example.com", password="testpassword")
        created_user = crud.create_user(db_session, user_data)
        
        # Get user by ID
        retrieved_user = crud.get_user_by_id(db_session, created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
    
    def test_get_user_by_id_not_found(self, db_session):
        """Test getting a non-existent user by ID."""
        user = crud.get_user_by_id(db_session, 999)
        assert user is None
    
    def test_get_user_by_email(self, db_session):
        """Test getting a user by email."""
        # Create a user
        user_data = schemas.UserCreate(email="test@example.com", password="testpassword")
        created_user = crud.create_user(db_session, user_data)
        
        # Get user by email
        retrieved_user = crud.get_user_by_email(db_session, "test@example.com")
        
        assert retrieved_user is not None
        assert retrieved_user.email == created_user.email
        assert retrieved_user.id == created_user.id
    
    def test_get_user_by_email_not_found(self, db_session):
        """Test getting a non-existent user by email."""
        user = crud.get_user_by_email(db_session, "nonexistent@example.com")
        assert user is None
    
    def test_get_users(self, db_session):
        """Test getting multiple users."""
        # Create multiple users
        for i in range(5):
            user_data = schemas.UserCreate(email=f"test{i}@example.com", password="testpassword")
            crud.create_user(db_session, user_data)
        
        # Get all users
        users = crud.get_users(db_session)
        assert len(users) == 5
        
        # Test pagination
        users_page1 = crud.get_users(db_session, skip=0, limit=2)
        users_page2 = crud.get_users(db_session, skip=2, limit=2)
        
        assert len(users_page1) == 2
        assert len(users_page2) == 2
        assert users_page1[0].id != users_page2[0].id
    
    def test_get_users_count(self, db_session):
        """Test getting the total count of users."""
        # Initially should be 0
        count = crud.get_users_count(db_session)
        assert count == 0
        
        # Create some users
        for i in range(3):
            user_data = schemas.UserCreate(email=f"test{i}@example.com", password="testpassword")
            crud.create_user(db_session, user_data)
        
        # Count should be 3
        count = crud.get_users_count(db_session)
        assert count == 3
    
    def test_update_user(self, db_session):
        """Test updating a user."""
        # Create a user
        user_data = schemas.UserCreate(email="test@example.com", password="testpassword")
        created_user = crud.create_user(db_session, user_data)
        
        # Update the user
        update_data = schemas.UserUpdate(email="updated@example.com", is_active=False)
        updated_user = crud.update_user(db_session, created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.email == "updated@example.com"
        assert updated_user.is_active is False
        assert updated_user.updated_at is not None
    
    def test_update_user_password(self, db_session):
        """Test updating a user's password."""
        # Create a user
        user_data = schemas.UserCreate(email="test@example.com", password="oldpassword")
        created_user = crud.create_user(db_session, user_data)
        old_hash = created_user.hashed_password
        
        # Update password
        update_data = schemas.UserUpdate(password="newpassword")
        updated_user = crud.update_user(db_session, created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.hashed_password != old_hash
        assert updated_user.hashed_password != "newpassword"  # Should be hashed
    
    def test_update_user_not_found(self, db_session):
        """Test updating a non-existent user."""
        update_data = schemas.UserUpdate(email="updated@example.com")
        updated_user = crud.update_user(db_session, 999, update_data)
        assert updated_user is None
    
    def test_delete_user(self, db_session):
        """Test deleting a user."""
        # Create a user
        user_data = schemas.UserCreate(email="test@example.com", password="testpassword")
        created_user = crud.create_user(db_session, user_data)
        
        # Delete the user
        success = crud.delete_user(db_session, created_user.id)
        assert success is True
        
        # Verify user is deleted
        deleted_user = crud.get_user_by_id(db_session, created_user.id)
        assert deleted_user is None
    
    def test_delete_user_not_found(self, db_session):
        """Test deleting a non-existent user."""
        success = crud.delete_user(db_session, 999)
        assert success is False
    
    def test_authenticate_user(self, db_session):
        """Test user authentication."""
        # Create a user
        user_data = schemas.UserCreate(email="test@example.com", password="testpassword")
        created_user = crud.create_user(db_session, user_data)
        
        # Test successful authentication
        authenticated_user = crud.authenticate_user(db_session, "test@example.com", "testpassword")
        assert authenticated_user is not None
        assert authenticated_user.id == created_user.id
        
        # Test failed authentication (wrong password)
        failed_auth = crud.authenticate_user(db_session, "test@example.com", "wrongpassword")
        assert failed_auth is None
        
        # Test failed authentication (wrong email)
        failed_auth = crud.authenticate_user(db_session, "wrong@example.com", "testpassword")
        assert failed_auth is None
    
    def test_password_hashing(self, db_session):
        """Test password hashing functionality."""
        password = "testpassword123"
        
        # Test hash_password function
        hashed = crud.hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
        
        # Test verify_password function
        assert crud.verify_password(password, hashed) is True
        assert crud.verify_password("wrongpassword", hashed) is False
        
        # Test that same password produces same hash
        hashed2 = crud.hash_password(password)
        assert hashed == hashed2 