from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field

class ResultDisplayConfig(SQLModel, table=True):
    __tablename__ = 'result_display_config'
    id: Optional[int] = Field(primary_key=True)
    displayId: str
    title: str
    key: str
    hidden: int
    sorter: int
    width: Optional[int] = None
    fixed: Optional[str] = None
    dataIndex: str
    sortIndex: int
    type: str
    ellipsis: Optional[int] = None
    align: Optional[str] = None
    dataType: Optional[str] = None
    format: Optional[str] = None
