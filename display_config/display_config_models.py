from typing import Optional, Dict, Any
from datetime import datetime

class GridMetadata:
    """Grid metadata model for managing grid configurations"""
    
    def __init__(self, id: Optional[int] = None, gridName: str = "", gridNameId: str = "", 
                 description: Optional[str] = None, is_active: int = 1,
                 created_at: Optional[str] = None, updated_at: Optional[str] = None):
        self.id = id
        self.gridName = gridName
        self.gridNameId = gridNameId
        self.description = description
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GridMetadata':
        """Create GridMetadata instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            gridName=data.get('gridName', ''),
            gridNameId=data.get('gridNameId', ''),
            description=data.get('description'),
            is_active=data.get('is_active', 1),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert GridMetadata instance to dictionary"""
        return {
            'id': self.id,
            'gridName': self.gridName,
            'gridNameId': self.gridNameId,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ResultDisplayConfig:
    """Result display configuration model for grid columns"""
    
    def __init__(self, id: Optional[int] = None, gridNameId: str = "", displayId: str = "", title: str = "", 
                 hidden: int = 0, width: Optional[int] = None, sortIndex: int = 0,
                 ellipsis: Optional[int] = None, align: Optional[str] = None,
                 dbDataType: Optional[str] = None, codeDataType: Optional[str] = None, format: Optional[str] = None,
                 created_at: Optional[str] = None, updated_at: Optional[str] = None):
        self.id = id
        self.gridNameId = gridNameId
        self.displayId = displayId
        self.title = title
        self.hidden = hidden
        self.width = width
        self.sortIndex = sortIndex
        self.ellipsis = ellipsis
        self.align = align
        self.dbDataType = dbDataType
        self.codeDataType = codeDataType
        self.format = format
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResultDisplayConfig':
        """Create ResultDisplayConfig instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            gridNameId=data.get('gridNameId', ''),
            displayId=data.get('displayId', ''),
            title=data.get('title', ''),
            hidden=data.get('hidden', 0),
            width=data.get('width'),
            sortIndex=data.get('sortIndex', 0),
            ellipsis=data.get('ellipsis'),
            align=data.get('align'),
            dbDataType=data.get('dbDataType'),
            codeDataType=data.get('codeDataType'),
            format=data.get('format'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ResultDisplayConfig instance to dictionary"""
        return {
            'id': self.id,
            'gridNameId': self.gridNameId,
            'displayId': self.displayId,
            'title': self.title,
            'hidden': self.hidden,
            'width': self.width,
            'sortIndex': self.sortIndex,
            'ellipsis': self.ellipsis,
            'align': self.align,
            'dbDataType': self.dbDataType,
            'codeDataType': self.codeDataType,
            'format': self.format,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }