"""
Authentication routes - User registration and login.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr

router = APIRouter()


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=Token)
async def register(user: UserRegister):
    """Register new user."""
    # TODO: Implement user registration
    # 1. Hash password
    # 2. Create user in database
    # 3. Generate JWT token
    return {"access_token": "mock_token", "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user."""
    # TODO: Implement login
    # 1. Verify credentials
    # 2. Generate JWT token
    return {"access_token": "mock_token", "token_type": "bearer"}


@router.get("/me")
async def get_current_user():
    """Get current user info."""
    # TODO: Implement with JWT verification
    return {"email": "user@example.com", "username": "user"}