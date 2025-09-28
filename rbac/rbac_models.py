from typing import Optional, Dict, Any
from datetime import datetime

class Role:
    """Role model for RBAC system with all original fields"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", display_name: str = "", 
                 description: str = "", is_active: bool = True, is_system_role: bool = False,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.description = description
        self.is_active = is_active
        self.is_system_role = is_system_role
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Role':
        """Create Role instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            display_name=data.get('display_name', ''),
            description=data.get('description', ''),
            is_active=bool(data.get('is_active', True)),
            is_system_role=bool(data.get('is_system_role', False)),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Role instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'is_active': self.is_active,
            'is_system_role': self.is_system_role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Right:
    """Right model for RBAC system with module support"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", display_name: str = "",
                 description: str = "", resource_type: str = "", resource_path: str = "",
                 http_method: Optional[str] = None, module: str = "default", 
                 is_active: bool = True, is_system_right: bool = False, 
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.description = description
        self.resource_type = resource_type
        self.resource_path = resource_path
        self.http_method = http_method
        self.module = module
        self.is_active = is_active
        self.is_system_right = is_system_right
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Right':
        """Create Right instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            display_name=data.get('display_name', ''),
            description=data.get('description', ''),
            resource_type=data.get('resource_type', ''),
            resource_path=data.get('resource_path', ''),
            http_method=data.get('http_method'),
            module=data.get('module', 'default'),
            is_active=bool(data.get('is_active', True)),
            is_system_right=bool(data.get('is_system_right', False)),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Right instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'resource_type': self.resource_type,
            'resource_path': self.resource_path,
            'http_method': self.http_method,
            'module': self.module,
            'is_active': self.is_active,
            'is_system_right': self.is_system_right,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RoleRight:
    """Role-Right assignment model for RBAC system with audit fields"""
    
    def __init__(self, id: Optional[int] = None, role_id: int = 0, right_id: int = 0,
                 granted_by: Optional[int] = None, granted_at: Optional[datetime] = None,
                 is_active: bool = True, created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.role_id = role_id
        self.right_id = right_id
        self.granted_by = granted_by
        self.granted_at = granted_at or datetime.now()
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RoleRight':
        """Create RoleRight instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            role_id=data.get('role_id', 0),
            right_id=data.get('right_id', 0),
            granted_by=data.get('granted_by'),
            granted_at=data.get('granted_at'),
            is_active=bool(data.get('is_active', True)),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert RoleRight instance to dictionary"""
        return {
            'id': self.id,
            'role_id': self.role_id,
            'right_id': self.right_id,
            'granted_by': self.granted_by,
            'granted_at': self.granted_at.isoformat() if self.granted_at else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }