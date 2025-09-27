from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str
    email: EmailStr
    phone: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    username_or_email: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    is_admin: bool


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"


class OTPRequest(BaseModel):
    """Schema for requesting an OTP"""
    username_or_email: str


class OTPVerify(BaseModel):
    """Schema for verifying an OTP"""
    username_or_email: str
    otp_code: str


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    username_or_email: str


class PasswordReset(BaseModel):
    """Schema for password reset"""
    username_or_email: str
    otp_code: str
    new_password: str = Field(..., min_length=8)


class MessageResponse(BaseModel):
    """Schema for message response"""
    message: str 