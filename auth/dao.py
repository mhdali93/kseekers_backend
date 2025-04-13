import time
import secrets

from manager.db_manager import DBSessionManager
from models.auth_models import User, OTP
from auth.query_helper import AuthQueryHelper
from utils.decorator import DecoratorUtils

class UserDAO:
    """Data Access Object for User operations"""
    
    def __init__(self):
        self.query_helper = AuthQueryHelper()
    
    def create_user(self, username, email, phone=None):
        """Create a new user"""
        with DBSessionManager() as session:
            # Check if user exists
            query = self.query_helper.check_existing_user_query(username, email)
            existing = session.exec(query).first()
            
            if existing:
                raise ValueError("User already exists")
            
            # Create user
            user = User(username=username, email=email, phone=phone)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    @DecoratorUtils.profile
    def get_user_by_username_or_email(self, username_or_email):
        """Get user by username or email"""
        with DBSessionManager() as session:
            query = self.query_helper.get_user_by_username_or_email_query(username_or_email)
            return session.exec(query).first()
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        with DBSessionManager() as session:
            query = self.query_helper.get_user_by_id_query(user_id)
            return session.exec(query).first()


class OTPDAO:
    """Data Access Object for OTP operations"""
    
    def __init__(self):
        self.query_helper = AuthQueryHelper()
    
    def create_otp(self, user_id):
        """Create a new OTP for the given user"""
        with DBSessionManager() as session:
            # Generate code
            code = f"{secrets.randbelow(1000000):06d}"
            
            # Create OTP record
            otp = OTP(
                user_id=user_id,
                code=code,
                expires_at=time.time() + 300,  # 5 minutes
                is_used=False
            )
            
            session.add(otp)
            session.commit()
            
            # Log for development (in production would send via SMS/email)
            DecoratorUtils.highlighted_print(f"*** OTP: {code} for user_id {user_id} ***")
            
            return code
        
    @DecoratorUtils.profile
    def verify_otp(self, user_id, code):
        """Verify an OTP code"""
        with DBSessionManager() as session:
            # Find latest OTP
            query = self.query_helper.get_latest_unused_otp_query(user_id, code)
            otp = session.exec(query).first()
            
            if not otp:
                return False
                
            # Check if expired
            if time.time() > otp.expires_at:
                return False
                
            # Mark as used
            otp.is_used = True
            session.add(otp)
            session.commit()
            
            return True 