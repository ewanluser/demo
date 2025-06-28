from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Base model for reading/returning user data
class UserBase(BaseModel):
    email: EmailStr

# Model for receiving data when creating a user (input)
class UserCreate(UserBase):
    password: str

# Model for updating user data
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# Model for returning data to the client from the database (output)
class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

# Response models
class UserResponse(BaseModel):
    message: str
    user: Optional[User] = None

class UsersListResponse(BaseModel):
    message: str
    users: List[User]
    total: int 