from fastapi import HTTPException
import logging

from auth.auth_models import User
from auth.dao import UserDAO, OTPDAO
from logical.jwt_auth import JWTHandler


class AuthController:
    """Controller for authentication business logic"""
    
    def __init__(self):
        self.user_dao = UserDAO()
        self.otp_dao = OTPDAO()
    
    def register_user(self, username, email, phone=None):
        """Register a new user"""
        try:
            user = self.user_dao.create_user(username, email, phone)
            logging.info(f"AUTH_CONTROLLER: User registered successfully - user_id={user.id}, username={username}")
            return user
        except Exception as e:
            logging.error(f"AUTH_CONTROLLER: User registration failed - username={username}, error={str(e)}")
            raise
    
    def get_user(self, username_or_email):
        """Get user by username or email"""
        try:
            user = self.user_dao.get_user_by_username_or_email(username_or_email)
            if not user:
                logging.warning(f"AUTH_CONTROLLER: User not found - username_or_email={username_or_email}")
            return user
        except Exception as e:
            logging.error(f"AUTH_CONTROLLER: Error looking up user - username_or_email={username_or_email}, error={str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.user_dao.get_user_by_id(user_id)
            if not user:
                logging.warning(f"AUTH_CONTROLLER: User not found - user_id={user_id}")
            return user
        except Exception as e:
            logging.error(f"AUTH_CONTROLLER: Error looking up user by ID - user_id={user_id}, error={str(e)}")
            raise
    
    def generate_otp(self, user_id):
        """Generate a new OTP for user"""
        try:
            otp_code = self.otp_dao.create_otp(user_id)
            logging.info(f"AUTH_CONTROLLER: OTP generated - user_id={user_id}, code={otp_code}")
            return otp_code
        except Exception as e:
            logging.error(f"AUTH_CONTROLLER: Error generating OTP - user_id={user_id}, error={str(e)}")
            raise
    
    def verify_otp(self, user_id, code):
        """Verify an OTP code"""
        try:
            is_valid = self.otp_dao.verify_otp(user_id, code)
            if not is_valid:
                logging.warning(f"AUTH_CONTROLLER: OTP verification failed - user_id={user_id}, code={code}")
            return is_valid
        except Exception as e:
            logging.error(f"AUTH_CONTROLLER: Error verifying OTP - user_id={user_id}, code={code}, error={str(e)}")
            raise
    
    def login(self, username_or_email, otp_code):
        """Login with username/email and OTP, return JWT token"""
        # Find user
        user = self.get_user(username_or_email)
        if not user:
            logging.error(f"AUTH_CONTROLLER: Login failed - User not found: {username_or_email}")
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify OTP
        if not self.verify_otp(user.id, otp_code):
            logging.error(f"AUTH_CONTROLLER: Login failed - Invalid OTP: user_id={user.id}, username={username_or_email}")
            raise HTTPException(status_code=401, detail="Invalid OTP")
        
        # Generate JWT token
        try:
            token = JWTHandler.create_token(user.id, user.username, user.is_admin)
            logging.info(f"AUTH_CONTROLLER: Login successful - user_id={user.id}, username={user.username}")
            return token
        except Exception as e:
            logging.error(f"AUTH_CONTROLLER: Login failed - JWT error: user_id={user.id}, error={str(e)}")
            raise
    
    def refresh_token(self, access_token):
        """Refresh an expired or soon-to-expire JWT token"""
        try:
            new_token = JWTHandler.refresh_token(access_token)
            if not new_token:
                logging.warning("AUTH_CONTROLLER: Token refresh failed - Invalid or too old token")
                raise HTTPException(status_code=401, detail="Token cannot be refreshed")
            
            logging.info("AUTH_CONTROLLER: Token refreshed successfully")
            return new_token
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"AUTH_CONTROLLER: Token refresh failed - error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error during token refresh") 