from functools import wraps
import time
import jwt
import logging
from typing import Dict, Any, Optional

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import config
from models.auth_models import TokenData
from models.enums import HTTPStatus

# JWT configuration
JWT_SECRET = config.secret
JWT_ALGORITHM = config.algorithm
JWT_EXPIRY = 15 * 60  # 15 minutes


class JWTHandler:
    """JWT token generation and verification"""
    
    @staticmethod
    def create_token(user_id, username, is_admin=False):
        """Create JWT token"""
        token_expiry = time.time() + JWT_EXPIRY
        
        # Create payload with both old and new fields for compatibility
        payload = {
            "user_id": user_id,
            "username": username,
            "is_admin": is_admin,
            "memberGUId": str(user_id),  # For legacy compatibility
            "expiry": token_expiry      # For legacy compatibility
        }
        
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def decode_token(token):
        """Decode and verify JWT token"""
        try:
            # Decode the token
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            # Check expiration - support both 'expiry' (old) and 'exp' (new) fields
            expiry_time = payload.get("expiry") or payload.get("exp", 0)
            if time.time() > expiry_time:
                return None
            
            # Create a unified payload with fields for both systems
            user_id = payload.get("user_id") or int(payload.get("memberGUId", 0))
            
            return {
                "user_id": user_id,
                "username": payload.get("username", ""),
                "is_admin": payload.get("is_admin", False),
                "memberGUId": str(user_id),
                "expiry": time.time() + JWT_EXPIRY  # Extend token life
            }
        except Exception as e:
            logging.error(f"Error decoding JWT: {e}")
            return None
    
    @staticmethod
    def token_response(token):
        """Format token for response"""
        return {"access_token": token, "token_type": "bearer"}


class JWTBearer(HTTPBearer):
    """JWT Bearer authentication for FastAPI"""
    
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        """Verify JWT token and extract user data"""
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not credentials or not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication"
            )
        
        # Decode and verify token
        payload = JWTHandler.decode_token(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or expired token"
            )
        
        # Create token data
        token_data = TokenData(
            user_id=payload.get("user_id"),
            username=payload.get("username", ""),
            is_admin=payload.get("is_admin", False)
        )
        
        # Store user info in request state
        request.state.user_id = token_data.user_id
        request.state.is_admin = token_data.is_admin
        
        return token_data


# Dependency to get the current user ID
def get_current_user_id(request: Request):
    """Get the current user ID from request state"""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user_id


# Dependency to check admin status
def admin_only(request: Request):
    """Check if the current user is an admin"""
    is_admin = getattr(request.state, "is_admin", False)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


# Decorator for jwt authentication (legacy compatibility)
def jwt_auth_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    async def authenticate(*args, **kwargs):
        request = kwargs.get('request')
        
        # Extract token from headers
        if 'Authorization' in request.headers or 'authorization' in request.headers:
            header = request.headers.get('Authorization') or request.headers.get('authorization')
            
            if header.startswith('Bearer '):
                token = header.split(" ")[1]
                payload = JWTHandler.decode_token(token)
                
                if payload:
                    # Store user info in request state
                    request.state.user_id = payload.get("user_id")
                    request.state.is_admin = payload.get("is_admin", False)
                    
                    # Add token to kwargs for compatibility
                    kwargs['token'] = token
                    return await f(*args, **kwargs)
                else:
                    raise HTTPException(
                        status_code=HTTPStatus.unauthorized.value[0],
                        detail="Invalid or expired token"
                    )
            else:
                raise HTTPException(
                    status_code=HTTPStatus.unauthorized.value[0],
                    detail="Invalid authorization format"
                )
        else:
            raise HTTPException(
                status_code=HTTPStatus.unauthorized.value[0],
                detail="Authorization header is missing"
            )
    
    return authenticate 