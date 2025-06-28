"""
Test cases for FastAPI User Management API endpoints.
"""

import pytest
from fastapi import status
from app import crud, schemas


class TestRootEndpoints:
    """Test root and health endpoints."""
    
    def test_read_root(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "redoc" in data
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "FastAPI User Management"


class TestUserEndpoints:
    """Test user management endpoints."""
    
    def test_create_user(self, client, sample_user_data):
        """Test creating a new user."""
        response = client.post("/users/", json=sample_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert "id" in data
        assert data["is_active"] is True
        assert "created_at" in data
        assert "hashed_password" not in data  # Should not return password
    
    def test_create_user_duplicate_email(self, client, sample_user_data):
        """Test creating a user with duplicate email should fail."""
        # Create first user
        client.post("/users/", json=sample_user_data)
        
        # Try to create second user with same email
        response = client.post("/users/", json=sample_user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_create_user_invalid_email(self, client):
        """Test creating a user with invalid email should fail."""
        invalid_data = {
            "email": "invalid-email",
            "password": "testpassword123"
        }
        response = client.post("/users/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_users(self, client, sample_user_data):
        """Test getting all users."""
        # Create a test user first
        client.post("/users/", json=sample_user_data)
        
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert "message" in data
        assert isinstance(data["users"], list)
        assert data["total"] >= 1
    
    def test_get_users_pagination(self, client, sample_user_data):
        """Test user pagination."""
        # Create multiple test users
        for i in range(3):
            user_data = {
                "email": f"test{i}@example.com",
                "password": "testpassword123"
            }
            client.post("/users/", json=user_data)
        
        # Test pagination
        response = client.get("/users/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data["users"]) <= 2
        assert data["total"] >= 3
    
    def test_get_user_by_id(self, client, sample_user_data):
        """Test getting a user by ID."""
        # Create a test user
        create_response = client.post("/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Get user by ID
        response = client.get(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == sample_user_data["email"]
    
    def test_get_user_by_id_not_found(self, client):
        """Test getting a non-existent user by ID."""
        response = client.get("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]
    
    def test_get_user_by_email(self, client, sample_user_data):
        """Test getting a user by email."""
        # Create a test user
        client.post("/users/", json=sample_user_data)
        
        # Get user by email
        response = client.get(f"/users/email/{sample_user_data['email']}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["email"] == sample_user_data["email"]
    
    def test_get_user_by_email_not_found(self, client):
        """Test getting a non-existent user by email."""
        response = client.get("/users/email/nonexistent@example.com")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]
    
    def test_update_user(self, client, sample_user_data, sample_user_update_data):
        """Test updating a user."""
        # Create a test user
        create_response = client.post("/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Update the user
        response = client.put(f"/users/{user_id}", json=sample_user_update_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == sample_user_update_data["email"]
        assert data["is_active"] == sample_user_update_data["is_active"]
        assert "updated_at" in data
    
    def test_update_user_not_found(self, client, sample_user_update_data):
        """Test updating a non-existent user."""
        response = client.put("/users/999", json=sample_user_update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]
    
    def test_update_user_duplicate_email(self, client, sample_user_data):
        """Test updating a user with an email that already exists."""
        # Create two users
        user1_data = {"email": "user1@example.com", "password": "password123"}
        user2_data = {"email": "user2@example.com", "password": "password123"}
        
        client.post("/users/", json=user1_data)
        create_response2 = client.post("/users/", json=user2_data)
        user2_id = create_response2.json()["id"]
        
        # Try to update user2 with user1's email
        update_data = {"email": "user1@example.com"}
        response = client.put(f"/users/{user2_id}", json=update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_delete_user(self, client, sample_user_data):
        """Test deleting a user."""
        # Create a test user
        create_response = client.post("/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        assert "User deleted successfully" in response.json()["message"]
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_user_not_found(self, client):
        """Test deleting a non-existent user."""
        response = client.delete("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_login_success(self, client, sample_user_data):
        """Test successful user login."""
        # Create a test user
        client.post("/users/", json=sample_user_data)
        
        # Login with correct credentials
        response = client.post("/auth/login", json=sample_user_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "user_id" in data
        assert "email" in data
        assert data["email"] == sample_user_data["email"]
    
    def test_login_wrong_password(self, client, sample_user_data):
        """Test login with wrong password."""
        # Create a test user
        client.post("/users/", json=sample_user_data)
        
        # Login with wrong password
        wrong_credentials = {
            "email": sample_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=wrong_credentials)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        credentials = {
            "email": "nonexistent@example.com",
            "password": "somepassword"
        }
        response = client.post("/auth/login", json=credentials)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_inactive_user(self, client, sample_user_data):
        """Test login with inactive user."""
        # Create a test user
        create_response = client.post("/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Deactivate the user
        client.put(f"/users/{user_id}", json={"is_active": False})
        
        # Try to login
        response = client.post("/auth/login", json=sample_user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Inactive user" in response.json()["detail"] 