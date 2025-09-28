from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """User model"""
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
    role_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "role_id": self.role_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


