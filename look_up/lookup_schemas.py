from pydantic import BaseModel
from typing import Optional, List

# Lookup Type Schemas
class LookupTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: str

class LookupTypeManageRequest(BaseModel):
    name: str
    description: Optional[str] = None

# Lookup Value Schemas
class LookupValueItem(BaseModel):
    code: str
    value: str
    description: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0

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
class LookupValuesByTypeRequest(BaseModel):
    type_name: str

class LookupValuesManageRequest(BaseModel):
    type_name: str
    values: List[LookupValueItem]
