from typing import Optional, Dict, Any, List
from datetime import datetime

class ContactUs:
    """Contact Us model for website contact form"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", email: str = "", 
                 phone: Optional[str] = None, whatsappNumber: Optional[str] = None, 
                 message: str = "", created_at: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.whatsappNumber = whatsappNumber
        self.message = message
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContactUs':
        """Create ContactUs instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone'),
            whatsappNumber=data.get('whatsappNumber'),
            message=data.get('message', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ContactUs instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'whatsappNumber': self.whatsappNumber,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PricingPlan:
    """Pricing Plan model for website pricing plans"""
    
    def __init__(self, id: Optional[int] = None, title: str = "", sessions: str = "", 
                 duration: str = "", base_price: float = 0.0, retention_discount: float = 0.0,
                 free_sessions: int = 0, curriculum: str = "", features: Optional[List[str]] = None,
                 is_current: bool = False, is_popular: bool = False, is_active: bool = True,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.title = title
        self.sessions = sessions
        self.duration = duration
        self.base_price = base_price
        self.retention_discount = retention_discount
        self.free_sessions = free_sessions
        self.curriculum = curriculum
        self.features = features or []
        self.is_current = is_current
        self.is_popular = is_popular
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PricingPlan':
        """Create PricingPlan instance from dictionary (database row)"""
        # Parse features from JSON string if stored as JSON
        features = data.get('features', [])
        if isinstance(features, str):
            import json
            try:
                features = json.loads(features)
            except (json.JSONDecodeError, TypeError):
                features = []
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            sessions=data.get('sessions', ''),
            duration=data.get('duration', ''),
            base_price=float(data.get('base_price', 0.0)),
            retention_discount=float(data.get('retention_discount', 0.0)),
            free_sessions=int(data.get('free_sessions', 0)),
            curriculum=data.get('curriculum', ''),
            features=features,
            is_current=bool(data.get('is_current', False)),
            is_popular=bool(data.get('is_popular', False)),
            is_active=bool(data.get('is_active', True)),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert PricingPlan instance to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'sessions': self.sessions,
            'duration': self.duration,
            'basePrice': self.base_price,
            'retentionDiscount': self.retention_discount,
            'freeSessions': self.free_sessions,
            'curriculum': self.curriculum,
            'features': self.features,
            'current': self.is_current,
            'popular': self.is_popular,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
