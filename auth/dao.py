import time
import secrets
from datetime import datetime, timedelta

from manager.db_manager import DBManager, get_db_transaction
from auth.auth_models import User, OTP
from auth.query_helper import AuthQueryHelper
from utils.decorator import DecoratorUtils

class UserDAO:
    """Data Access Object for User operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    def create_user(self, username, email, phone=None):
        """Create a new user"""
        # Check if user exists
        existing = self.get_user_by_username_or_email(username)
        if existing:
            raise ValueError("User already exists")
        
        existing = self.get_user_by_username_or_email(email)
        if existing:
            raise ValueError("User already exists")
        
        # Create user using query helper
        query = AuthQueryHelper.create_user_query()
        now = datetime.now()
        user_id = self.db_manager.execute_insert(query, (
            username, email, phone, True, False, now, now
        ))
        
        return User(id=user_id, username=username, email=email, phone=phone)
    
    @DecoratorUtils.profile
    def get_user_by_username_or_email(self, username_or_email):
        """Get user by username or email"""
        query = AuthQueryHelper.get_user_by_username_or_email_query()
        result = self.db_manager.execute_query(query, (username_or_email, username_or_email))
        
        if result:
            return User.from_dict(result[0])
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        query = AuthQueryHelper.get_user_by_id_query()
        result = self.db_manager.execute_query(query, (user_id,))
        
        if result:
            return User.from_dict(result[0])
        return None


class OTPDAO:
    """Data Access Object for OTP operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    def create_otp(self, user_id):
        """Create a new OTP for the given user"""
        # Generate code
        code = f"{secrets.randbelow(1000000):06d}"
        code = "123456"
        
        # Create OTP record using query helper
        expires_at = datetime.now() + timedelta(minutes=5)
        query = AuthQueryHelper.create_otp_query()
        now = datetime.now()
        self.db_manager.execute_insert(query, (
            user_id, code, expires_at, False, now
        ))
        
        # Log for development (in production would send via SMS/email)
        DecoratorUtils.highlighted_print(f"*** OTP: {code} for user_id {user_id} ***")
        
        return code
        
    @DecoratorUtils.profile
    def verify_otp(self, user_id, code):
        """Verify an OTP code"""
        # Find latest OTP using query helper
        query = AuthQueryHelper.get_latest_unused_otp_query()
        result = self.db_manager.execute_query(query, (user_id, code))
        
        if not result:
            return False
        
        otp_data = result[0]
        otp = OTP.from_dict(otp_data)
        
        # Check if expired
        if datetime.now() > otp.expires_at:
            return False
            
        # Mark as used using query helper
        update_query = AuthQueryHelper.mark_otp_as_used_query()
        self.db_manager.execute_update(update_query, (otp.id,))
        
        return True 