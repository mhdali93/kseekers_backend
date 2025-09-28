from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from rbac.rbac_models import Right, Role


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    is_active: bool = True
    is_admin: bool = False
    role_id: Optional[int] = None


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    user_id: int = Field(..., description="ID of the user to update")
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    role_id: Optional[int] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    is_active: bool
    is_admin: bool
    role_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserListResponse(BaseModel):
    """Schema for user list response"""
    users: List[UserResponse]
    total: int
    page: int
    per_page: int


class RightResponse(BaseModel):
    """Schema for right response (rights come through user's role)"""
    id: int
    name: str
    display_name: str
    description: Optional[str] = None
    resource_type: Optional[str] = None
    resource_path: Optional[str] = None
    http_method: Optional[str] = None
    module: Optional[str] = None
    is_active: bool


class RoleResponse(BaseModel):
    """Schema for role response"""
    id: int
    name: str
    display_name: str
    description: Optional[str] = None
    is_active: bool
    is_system_role: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserRightsResponse(BaseModel):
    """Schema for user rights response (rights inherited through role)"""
    user_id: int
    username: str
    role_id: Optional[int] = None
    role_name: Optional[str] = None
    rights: List[RightResponse]


class UserApiAccessRequest(BaseModel):
    """Schema for checking user API access"""
    user_id: int = Field(..., description="ID of the user to check access for")
    resource_path: str
    http_method: Optional[str] = "GET"


class UserApiAccessResponse(BaseModel):
    """Schema for user API access response"""
    has_access: bool
    right_name: Optional[str] = None
    right_display_name: Optional[str] = None
    module: Optional[str] = None


class MessageResponse(BaseModel):
    """Schema for message response"""
    message: str
