from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
import time

class User(SQLModel, table=True):
    """User model for authentication"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    phone: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class OTP(SQLModel, table=True):
    """OTP model for authentication"""
    __tablename__ = "otps"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    code: str
    expires_at: float  # Expiration time as Unix timestamp
    is_used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

class TokenData(SQLModel):
    """Model for JWT token data"""
    user_id: int
    username: str
    is_admin: bool = False
    exp: Optional[float] = None 