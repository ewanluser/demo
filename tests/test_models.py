"""
Test cases for database models.
"""

import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models import User


class TestUserModel:
    """Test User model."""
    
    def test_create_user(self, db_session):
        """Test creating a user model."""
        user = User(
            email="test@example.com",
            hashed_password="hashedpassword123",
            is_active=True
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashedpassword123"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
        assert user.updated_at is None  # Should be None initially
    
    def test_user_email_unique_constraint(self, db_session):
        """Test that email must be unique."""
        # Create first user
        user1 = User(
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        db_session.add(user1)
        db_session.commit()
        
        # Try to create second user with same email
        user2 = User(
            email="test@example.com",
            hashed_password="anotherhashedpassword"
        )
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_email_not_null(self, db_session):
        """Test that email cannot be null."""
        user = User(
            hashed_password="hashedpassword123"
        )
        db_session.add(user)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_hashed_password_not_null(self, db_session):
        """Test that hashed_password cannot be null."""
        user = User(
            email="test@example.com"
        )
        db_session.add(user)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_is_active_default(self, db_session):
        """Test that is_active defaults to True."""
        user = User(
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.is_active is True
    
    def test_user_timestamps(self, db_session):
        """Test user timestamp fields."""
        user = User(
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Check created_at is set
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
        
        # Check updated_at is initially None
        assert user.updated_at is None
        
        # Update the user
        original_created_at = user.created_at
        user.email = "updated@example.com"
        db_session.commit()
        db_session.refresh(user)
        
        # Check updated_at is now set
        assert user.updated_at is not None
        assert isinstance(user.updated_at, datetime)
        assert user.updated_at >= original_created_at
        
        # Check created_at hasn't changed
        assert user.created_at == original_created_at
    
    def test_user_string_representation(self, db_session):
        """Test user model string representation."""
        user = User(
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # The model doesn't have __str__ or __repr__ defined,
        # but we can test that it doesn't raise an error
        str_repr = str(user)
        assert "User" in str_repr 