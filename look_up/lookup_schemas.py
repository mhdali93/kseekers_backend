from pydantic import BaseModel
from typing import Optional, List

# Lookup Type Schemas
class LookupTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None

class LookupTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class LookupTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: str

# Lookup Value Schemas
class LookupValueCreate(BaseModel):
    lookup_type_id: int
    code: str
    value: str
    description: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0

class LookupValueUpdate(BaseModel):
    code: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class LookupValueResponse(BaseModel):
    id: int
    lookup_type_id: int
    code: str
    value: str
    description: Optional[str] = None
    is_active: bool
    sort_order: int
    created_at: str

# Request Schemas for API endpoints
class LookupByTypeRequest(BaseModel):
    type: str

class LookupValuesByTypeRequest(BaseModel):
    lookup_type_name: str

class LookupTypeGetRequest(BaseModel):
    type: str

class LookupTypeUpdateRequest(BaseModel):
    type_id: int
    name: Optional[str] = None
    description: Optional[str] = None

class LookupTypeDeleteRequest(BaseModel):
    type_id: int

class LookupValueGetRequest(BaseModel):
    value_id: int

class LookupValueUpdateRequest(BaseModel):
    value_id: int
    code: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class LookupValueDeleteRequest(BaseModel):
    value_id: int

# Response Schemas for API endpoints
class LookupTypeListResponse(BaseModel):
    data: List[LookupTypeResponse]
    total: int

class LookupValueListResponse(BaseModel):
    data: List[LookupValueResponse]
    total: int
