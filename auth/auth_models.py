from typing import Optional, Dict, Any
from datetime import datetime
import time

class User:
    """User model for authentication"""
    
    def __init__(self, id: Optional[int] = None, username: str = "", email: str = "", 
                 phone: Optional[str] = None, is_active: bool = True, 
                 is_admin: bool = False, created_at: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.username = username
        self.email = email
        self.phone = phone
        self.is_active = is_active
        self.is_admin = is_admin
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            email=data.get('email', ''),
            phone=data.get('phone'),
            is_active=bool(data.get('is_active', True)),
            is_admin=bool(data.get('is_admin', False)),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert User instance to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class OTP:
    """OTP model for authentication"""
    
    def __init__(self, id: Optional[int] = None, user_id: int = 0, code: str = "", 
                 expires_at: Optional[datetime] = None, is_used: bool = False, 
                 created_at: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.code = code
        self.expires_at = expires_at or datetime.now()
        self.is_used = is_used
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OTP':
        """Create OTP instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id', 0),
            code=data.get('code', ''),
            expires_at=data.get('expires_at'),
            is_used=bool(data.get('is_used', False)),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert OTP instance to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'code': self.code,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_used': self.is_used,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TokenData:
    """Model for JWT token data"""
    
    def __init__(self, user_id: int, username: str, is_admin: bool = False, exp: Optional[float] = None):
        self.user_id = user_id
        self.username = username
        self.is_admin = is_admin
        self.exp = exp 