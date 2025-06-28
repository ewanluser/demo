"""
Test cases for Pydantic schemas.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app import schemas


class TestUserSchemas:
    """Test user Pydantic schemas."""
    
    def test_user_base_valid(self):
        """Test UserBase schema with valid data."""
        user_data = {"email": "test@example.com"}
        user = schemas.UserBase(**user_data)
        
        assert user.email == "test@example.com"
    
    def test_user_base_invalid_email(self):
        """Test UserBase schema with invalid email."""
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserBase(email="invalid-email")
        
        assert "value is not a valid email address" in str(exc_info.value)
    
    def test_user_create_valid(self):
        """Test UserCreate schema with valid data."""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        user = schemas.UserCreate(**user_data)
        
        assert user.email == "test@example.com"
        assert user.password == "testpassword123"
    
    def test_user_create_missing_password(self):
        """Test UserCreate schema with missing password."""
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserCreate(email="test@example.com")
        
        assert "Field required" in str(exc_info.value)
    
    def test_user_update_valid(self):
        """Test UserUpdate schema with valid data."""
        update_data = {
            "email": "updated@example.com",
            "password": "newpassword",
            "is_active": False
        }
        user_update = schemas.UserUpdate(**update_data)
        
        assert user_update.email == "updated@example.com"
        assert user_update.password == "newpassword"
        assert user_update.is_active is False
    
    def test_user_update_partial(self):
        """Test UserUpdate schema with partial data."""
        # Should allow partial updates
        user_update = schemas.UserUpdate(email="updated@example.com")
        assert user_update.email == "updated@example.com"
        assert user_update.password is None
        assert user_update.is_active is None
        
        # Should allow empty updates
        user_update = schemas.UserUpdate()
        assert user_update.email is None
        assert user_update.password is None
        assert user_update.is_active is None
    
    def test_user_response_valid(self):
        """Test User response schema with valid data."""
        user_data = {
            "email": "test@example.com",
            "id": 1,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
        user = schemas.User(**user_data)
        
        assert user.email == "test@example.com"
        assert user.id == 1
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
        assert user.updated_at is None
    
    def test_user_response_missing_required_fields(self):
        """Test User response schema with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            schemas.User(email="test@example.com")
        
        error_str = str(exc_info.value)
        assert "Field required" in error_str
    
    def test_user_response_model(self):
        """Test UserResponse schema."""
        user_data = {
            "email": "test@example.com",
            "id": 1,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
        user = schemas.User(**user_data)
        
        response_data = {
            "message": "User created successfully",
            "user": user
        }
        response = schemas.UserResponse(**response_data)
        
        assert response.message == "User created successfully"
        assert response.user.email == "test@example.com"
        
        # Test with no user
        response_no_user = schemas.UserResponse(message="No user found")
        assert response_no_user.message == "No user found"
        assert response_no_user.user is None
    
    def test_users_list_response(self):
        """Test UsersListResponse schema."""
        user_data = {
            "email": "test@example.com",
            "id": 1,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
        user = schemas.User(**user_data)
        
        response_data = {
            "message": "Users retrieved successfully",
            "users": [user],
            "total": 1
        }
        response = schemas.UsersListResponse(**response_data)
        
        assert response.message == "Users retrieved successfully"
        assert len(response.users) == 1
        assert response.users[0].email == "test@example.com"
        assert response.total == 1
        
        # Test with empty list
        empty_response = schemas.UsersListResponse(
            message="No users found",
            users=[],
            total=0
        )
        assert empty_response.message == "No users found"
        assert len(empty_response.users) == 0
        assert empty_response.total == 0
    
    def test_schema_json_serialization(self):
        """Test that schemas can be serialized to JSON."""
        user_data = {
            "email": "test@example.com",
            "id": 1,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
        user = schemas.User(**user_data)
        
        # Should be able to convert to dict
        user_dict = user.model_dump()
        assert isinstance(user_dict, dict)
        assert user_dict["email"] == "test@example.com"
        
        # Should be able to convert to JSON
        user_json = user.model_dump_json()
        assert isinstance(user_json, str)
        assert "test@example.com" in user_json 