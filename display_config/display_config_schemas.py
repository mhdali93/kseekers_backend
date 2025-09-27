from pydantic import BaseModel
from typing import Optional, List

# Grid Metadata Schemas
class GridMetadataCreate(BaseModel):
    gridName: str
    gridNameId: str
    description: Optional[str] = None
    is_active: int = 1

class GridMetadataUpdate(BaseModel):
    gridName: Optional[str] = None
    gridNameId: Optional[str] = None
    description: Optional[str] = None
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
class ResultDisplayConfigCreate(BaseModel):
    gridNameId: str
    displayId: str
    title: str
    hidden: int = 0
    width: Optional[int] = None
    sortIndex: int
    ellipsis: Optional[int] = None
    align: Optional[str] = None
    dbDataType: Optional[str] = None
    codeDataType: Optional[str] = None
    format: Optional[str] = None

class ResultDisplayConfigUpdate(BaseModel):
    gridNameId: Optional[str] = None
    displayId: Optional[str] = None
    title: Optional[str] = None
    hidden: Optional[int] = None
    width: Optional[int] = None
    sortIndex: Optional[int] = None
    ellipsis: Optional[int] = None
    align: Optional[str] = None
    dbDataType: Optional[str] = None
    codeDataType: Optional[str] = None
    format: Optional[str] = None

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

class ResultDisplayConfigListResponse(BaseModel):
    configs: List[ResultDisplayConfigResponse]

class ResultDisplayConfigByGridRequest(BaseModel):
    gridNameId: str

class GridHeadersRequest(BaseModel):
    gridNameId: str

class DisplayConfigByTypeRequest(BaseModel):
    type: str

class DisplayConfigByIdRequest(BaseModel):
    id: int

class GridHeadersResponse(BaseModel):
    headers: List[ResultDisplayConfigResponse]

class DisplayConfigGetRequest(BaseModel):
    config_id: int

class DisplayConfigUpdateRequest(BaseModel):
    config_id: int
    gridNameId: Optional[str] = None
    displayId: Optional[str] = None
    title: Optional[str] = None
    hidden: Optional[int] = None
    width: Optional[int] = None
    sortIndex: Optional[int] = None
    ellipsis: Optional[int] = None
    align: Optional[str] = None
    dbDataType: Optional[str] = None
    codeDataType: Optional[str] = None
    format: Optional[str] = None

class DisplayConfigDeleteRequest(BaseModel):
    config_id: int