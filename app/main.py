from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(
    title="FastAPI User Management",
    description="A high-concurrency API built with FastAPI, SQLAlchemy, and Alembic",
    version="1.0.0"
)

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint to check if the API is running."""
    return {
        "message": "FastAPI User Management API is running!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "FastAPI User Management"}

# User endpoints
@app.post("/users/", response_model=schemas.User, tags=["Users"], status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=schemas.UsersListResponse, tags=["Users"])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    db: Session = Depends(get_db)
):
    """Get a list of all users with pagination."""
    users = crud.get_users(db, skip=skip, limit=limit)
    total = crud.get_users_count(db)
    return schemas.UsersListResponse(
        message=f"Retrieved {len(users)} users",
        users=users,
        total=total
    )

@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by their ID."""
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
async def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db)
):
    """Update a specific user."""
    # Check if email is being updated and already exists
    if user_update.email:
        existing_user = crud.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user"
            )
    
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user

@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a specific user."""
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return {"message": "User deleted successfully"}

@app.post("/auth/login", tags=["Authentication"])
async def login(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    """Authenticate a user with email and password."""
    user = crud.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email
    }

# Additional utility endpoints
@app.get("/users/email/{email}", response_model=schemas.User, tags=["Users"])
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Get a user by their email address."""
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 