from pydantic import BaseModel
from typing import Optional, List

# Grid Metadata Schemas
class GridMetadataCreate(BaseModel):
    gridName: str
    gridNameId: str
    description: Optional[str] = None

class GridMetadataUpdate(BaseModel):
    id: int
    gridName: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None

class GridMetadataListRequest(BaseModel):
    name: Optional[str] = None
    is_active: Optional[int] = None

class GridMetadataResponse(BaseModel):
    id: int
    gridName: str
    gridNameId: str
    description: Optional[str] = None
    is_active: int
    created_at: str
    updated_at: str

# Result Display Config Schemas
class ResultDisplayConfigItem(BaseModel):
    displayId: str
    title: str
    hidden: int = 0
    width: Optional[int] = None
    sortIndex: int = 0
    ellipsis: Optional[int] = None
    align: Optional[str] = None
    dbDataType: Optional[str] = None
    codeDataType: Optional[str] = None
    format: Optional[str] = None

class ResultDisplayConfigListRequest(BaseModel):
    gridNameId: str

class ResultDisplayConfigUpdateRequest(BaseModel):
    gridNameId: str
    configs: List[ResultDisplayConfigItem]

class ResultDisplayConfigResponse(BaseModel):
    id: int
    gridNameId: str
    displayId: str
    title: str
    hidden: int
    width: Optional[int] = None
    sortIndex: int
    ellipsis: Optional[int] = None
    align: Optional[str] = None
    dbDataType: Optional[str] = None
    codeDataType: Optional[str] = None
    format: Optional[str] = None
    created_at: str
    updated_at: str