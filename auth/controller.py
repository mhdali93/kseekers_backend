from fastapi import HTTPException

from models.auth_models import User
from auth.dao import UserDAO, OTPDAO
from logical.jwt_auth import JWTHandler


class AuthController:
    """Controller for authentication business logic"""
    
    def __init__(self):
        self.user_dao = UserDAO()
        self.otp_dao = OTPDAO()
    
    def register_user(self, username, email, phone=None):
        """Register a new user"""
        return self.user_dao.create_user(username, email, phone)
    
    def get_user(self, username_or_email):
        """Get user by username or email"""
        return self.user_dao.get_user_by_username_or_email(username_or_email)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.user_dao.get_user_by_id(user_id)
    
    def generate_otp(self, user_id):
        """Generate a new OTP for user"""
        return self.otp_dao.create_otp(user_id)
    
    def verify_otp(self, user_id, code):
        """Verify an OTP code"""
        return self.otp_dao.verify_otp(user_id, code)
    
    def login(self, username_or_email, otp_code):
        """Login with username/email and OTP, return JWT token"""
        # Find user
        user = self.get_user(username_or_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify OTP
        if not self.verify_otp(user.id, otp_code):
            raise HTTPException(status_code=401, detail="Invalid OTP")
        
        # Generate JWT token
        return JWTHandler.create_token(user.id, user.username, user.is_admin) 