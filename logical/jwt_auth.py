from functools import wraps
import time
import jwt
import logging
from typing import Dict, Any, Optional

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import config
from auth.auth_models import TokenData
from models.enums import HTTPStatus

# JWT configuration
JWT_SECRET = config.secret
JWT_ALGORITHM = config.algorithm
JWT_EXPIRY = config.expiry


class JWTHandler:
    """JWT token generation and verification"""
    
    @staticmethod
    def create_token(user_id, username, is_admin=False):
        """Create JWT token"""
        try:
            token_expiry = time.time() + JWT_EXPIRY
            
            # Create payload with both old and new fields for compatibility
            payload = {
                "user_id": user_id,
                "username": username,
                "is_admin": is_admin,
                "memberGUId": str(user_id),  # For legacy compatibility
                "expiry": token_expiry      # For legacy compatibility
            }
            
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            logging.info(f"JWT_HANDLER: Token created - user_id={user_id}, username={username}")
            
            return token
        except Exception as e:
            logging.error(f"JWT_HANDLER: Error creating token - user_id={user_id}, error={str(e)}")
            raise
    
    @staticmethod
    def decode_token(token):
        """Decode and verify JWT token"""
        try:
            # Decode the token
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            # Check expiration - support both 'expiry' (old) and 'exp' (new) fields
            expiry_time = payload.get("expiry") or payload.get("exp", 0)
            current_time = time.time()

            logging.info(f"JWT_HANDLER: expiry_time={expiry_time}, current_time={current_time}, time left={expiry_time - current_time}")
            
            if current_time > expiry_time:
                logging.warning(f"JWT_HANDLER: Token expired - user_id={payload.get('user_id', 'unknown')}")
                return None
            
            # Create a unified payload with fields for both systems
            user_id = payload.get("user_id") or int(payload.get("memberGUId", 0))
            
            token_data = {
                "user_id": user_id,
                "username": payload.get("username", ""),
                "is_admin": payload.get("is_admin", False),
                "memberGUId": str(user_id),
                "expiry": time.time() + JWT_EXPIRY  # Extend token life
            }
            
            return token_data
        except Exception as e:
            logging.error(f"JWT_HANDLER: Error decoding JWT: {e}")
            return None
    
    @staticmethod
    def decode_token_for_refresh(token):
        """Decode token for refresh purposes - allows expired tokens but validates signature"""
        try:
            # Decode the token without checking expiration
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
            
            # Get expiry time
            expiry_time = payload.get("expiry") or payload.get("exp", 0)
            current_time = time.time()
            
            # Check if token is within refresh window (1 hour before expiry)
            refresh_window = JWT_EXPIRY / 2  # 1 hour if JWT_EXPIRY is 2 hours
            time_until_expiry = expiry_time - current_time
            
            # If token is expired but within refresh window, allow refresh
            if time_until_expiry < -refresh_window:
                logging.warning(f"JWT_HANDLER: Token too old for refresh - user_id={payload.get('user_id', 'unknown')}")
                return None
            
            # Create a unified payload with fields for both systems
            user_id = payload.get("user_id") or int(payload.get("memberGUId", 0))
            
            token_data = {
                "user_id": user_id,
                "username": payload.get("username", ""),
                "is_admin": payload.get("is_admin", False),
                "memberGUId": str(user_id),
                "expiry": expiry_time,
                "is_expired": current_time > expiry_time
            }
            
            return token_data
        except Exception as e:
            logging.error(f"JWT_HANDLER: Error decoding JWT for refresh: {e}")
            return None
    
    @staticmethod
    def refresh_token(token):
        """Refresh an expired or soon-to-expire token"""
        try:
            # Decode token for refresh (allows expired tokens)
            token_data = JWTHandler.decode_token_for_refresh(token)
            if not token_data:
                logging.warning("JWT_HANDLER: Invalid token for refresh")
                return None
            
            # Generate new token with same user data
            new_token = JWTHandler.create_token(
                user_id=token_data["user_id"],
                username=token_data["username"],
                is_admin=token_data["is_admin"]
            )
            
            logging.info(f"JWT_HANDLER: Token refreshed successfully - user_id={token_data['user_id']}")
            return new_token
        except Exception as e:
            logging.error(f"JWT_HANDLER: Error refreshing token: {e}")
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
        credentials = await super().__call__(request)
        
        if not credentials or not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        # Decode and verify token
        payload = JWTHandler.decode_token(credentials.credentials)
        if not payload:
            # Try to decode for refresh to provide better error message
            refresh_payload = JWTHandler.decode_token_for_refresh(credentials.credentials)
            if refresh_payload and refresh_payload.get("is_expired"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Token expired"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Not authenticated"
                )
        
        # Create token data
        user_id = payload.get("user_id")
        if not isinstance(user_id, int):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        token_data = TokenData(
            user_id=user_id,
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
        if not request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request object not found"
            )
        
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
                    # Try to decode for refresh to provide better error message
                    refresh_payload = JWTHandler.decode_token_for_refresh(token)
                    if refresh_payload and refresh_payload.get("is_expired"):
                        raise HTTPException(
                            status_code=HTTPStatus.unauthorized.value[0],
                            detail="Token expired"
                        )
                    else:
                        raise HTTPException(
                            status_code=HTTPStatus.unauthorized.value[0],
                            detail="Not authenticated"
                        )
            else:
                raise HTTPException(
                    status_code=HTTPStatus.unauthorized.value[0],
                    detail="Not authenticated"
                )
        else:
            raise HTTPException(
                status_code=HTTPStatus.unauthorized.value[0],
                detail="Not authenticated"
            )
    
    return authenticate 