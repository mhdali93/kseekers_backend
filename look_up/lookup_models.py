from typing import Optional, Dict, Any
from datetime import datetime

class LookupType:
    """Lookup type model for categories"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", description: str = "", 
                 created_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LookupType':
        """Create LookupType instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            description=data.get('description', ''),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert LookupType instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LookupValue:
    """Lookup value model for key-value pairs"""
    
    def __init__(self, id: Optional[int] = None, lookup_type_id: int = 0, code: str = "", 
                 value: str = "", description: str = "", is_active: bool = True, 
                 sort_order: int = 0, created_at: Optional[datetime] = None):
        self.id = id
        self.lookup_type_id = lookup_type_id
        self.code = code
        self.value = value
        self.description = description
        self.is_active = is_active
        self.sort_order = sort_order
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LookupValue':
        """Create LookupValue instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            lookup_type_id=data.get('lookup_type_id', 0),
            code=data.get('code', ''),
            value=data.get('value', ''),
            description=data.get('description', ''),
            is_active=bool(data.get('is_active', True)),
            sort_order=data.get('sort_order', 0),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert LookupValue instance to dictionary"""
        return {
            'id': self.id,
            'lookup_type_id': self.lookup_type_id,
            'code': self.code,
            'value': self.value,
            'description': self.description,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

