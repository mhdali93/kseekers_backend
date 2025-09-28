from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Role Schemas
class RoleCreate(BaseModel):
    """Schema for creating a new role"""
    name: str = Field(..., min_length=2, max_length=100, description="Role name (unique identifier)")
    display_name: str = Field(..., min_length=2, max_length=255, description="Human-readable role name")
    description: Optional[str] = Field(None, description="Role description")
    is_active: bool = Field(True, description="Whether the role is active")

class RoleUpdate(BaseModel):
    """Schema for updating a role"""
    id: int = Field(..., gt=0, description="Role ID")
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    display_name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None

class RoleResponse(BaseModel):
    """Schema for role response"""
    id: int
    name: str
    display_name: str
    description: Optional[str] = None
    is_active: bool
    is_system_role: bool
    created_at: datetime
    updated_at: datetime

class RoleListRequest(BaseModel):
    """Schema for role list request with filters"""
    name: Optional[str] = Field(None, description="Filter by role name")
    is_active: Optional[bool] = Field(None, description="Filter by active status")

# Right Schemas
class RightCreate(BaseModel):
    """Schema for creating a new right"""
    name: str = Field(..., min_length=1, max_length=100, description="Right name (unique identifier)")
    display_name: str = Field(..., min_length=2, max_length=255, description="Human-readable right name")
    description: Optional[str] = Field(None, description="Right description")
    resource_type: str = Field(..., description="Type of resource (ui_page, api_endpoint, feature, action)")
    resource_path: str = Field(..., min_length=1, max_length=500, description="Resource path or identifier")
    http_method: Optional[str] = Field(None, max_length=10, description="HTTP method for API endpoints")
    module: str = Field(..., min_length=1, max_length=100, description="Module this right belongs to")
    is_active: bool = Field(True, description="Whether the right is active")

class RightUpdate(BaseModel):
    """Schema for updating a right"""
    id: int = Field(..., gt=0, description="Right ID")
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    display_name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    resource_type: Optional[str] = None
    resource_path: Optional[str] = Field(None, min_length=1, max_length=500)
    http_method: Optional[str] = Field(None, max_length=10)
    module: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None

class RightResponse(BaseModel):
    """Schema for right response"""
    id: int
    name: str
    display_name: str
    description: Optional[str] = None
    resource_type: str
    resource_path: str
    http_method: Optional[str] = None
    module: str
    is_active: bool
    is_system_right: bool
    created_at: datetime
    updated_at: datetime

class RightListRequest(BaseModel):
    """Schema for right list request with filters"""
    name: Optional[str] = Field(None, description="Filter by right name")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    module: Optional[str] = Field(None, description="Filter by module")

# Role-Rights Management Schemas
class RoleRightsRequest(BaseModel):
    """Schema for getting role rights"""
    role_id: int = Field(..., gt=0, description="Role ID")

class RoleRightsManageRequest(BaseModel):
    """Schema for managing role rights"""
    role_id: int = Field(..., gt=0, description="Role ID")
    right_ids: List[int] = Field(..., min_items=0, description="List of right IDs to assign to role")

class RoleRightResponse(BaseModel):
    """Schema for role right response"""
    id: int
    role_id: int
    right_id: int
    right_name: str
    right_display_name: str
    right_description: Optional[str] = None
    resource_type: str
    resource_path: str
    http_method: Optional[str] = None
    module: str
    granted_by: Optional[int] = None
    granted_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime

# User Rights Schemas
class UserRightsRequest(BaseModel):
    """Schema for user rights request"""
    user_id: int = Field(..., gt=0, description="User ID")

class UserApiAccessRequest(BaseModel):
    """Schema for user API access check"""
    user_id: int = Field(..., gt=0, description="User ID")
    api_path: str = Field(..., min_length=1, description="API path to check access for")

class UserRightResponse(BaseModel):
    """Schema for user right response"""
    id: int
    name: str
    display_name: str
    description: Optional[str] = None
    resource_type: str
    resource_path: str
    http_method: Optional[str] = None
    module: str

class ApiAccessResponse(BaseModel):
    """Schema for API access response"""
    user_id: int
    api_path: str
    has_access: bool
    right_name: Optional[str] = None
    right_display_name: Optional[str] = None
    right_description: Optional[str] = None
    module: Optional[str] = None

# Module Schemas
class ModuleRightsRequest(BaseModel):
    """Schema for getting module rights"""
    module: str = Field(..., min_length=1, description="Module name")

class ModuleRightsResponse(BaseModel):
    """Schema for module rights response"""
    module: str
    rights: List[RightResponse]
    has_wildcard_access: bool