from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class ContactUsRequest(BaseModel):
    """Schema for contact us form submission"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    whatsappNumber: Optional[str] = Field(None, max_length=20)
    message: str = Field(..., min_length=1, max_length=1000)


class ContactUsResponse(BaseModel):
    """Schema for contact us response"""
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    whatsappNumber: Optional[str] = None
    message: str
    created_at: str


class PricingPlanResponse(BaseModel):
    """Schema for pricing plan response"""
    id: int
    title: str
    sessions: str
    duration: str
    basePrice: float
    retentionDiscount: float
    freeSessions: int
    curriculum: str
    features: List[str]
    current: bool
    popular: bool
    is_active: bool


class MessageResponse(BaseModel):
    """Schema for message response"""
    message: str
