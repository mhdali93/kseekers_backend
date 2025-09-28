import time
import secrets
from datetime import datetime, timedelta
import logging

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
            logging.error(f"USER_DAO: Username already exists: {username}")
            raise ValueError("User already exists")
        
        existing = self.get_user_by_username_or_email(email)
        if existing:
            logging.error(f"USER_DAO: Email already exists: {email}")
            raise ValueError("User already exists")
        
        # Create user using query helper
        now = datetime.now()
        try:
            query, values = AuthQueryHelper.create_user_query(
                username=username, email=email, phone=phone, 
                is_active=True, is_admin=False, created_at=now, updated_at=now
            )
            user_id = self.db_manager.execute_insert(query, values)
            logging.info(f"USER_DAO: User created - user_id={user_id}, username={username}")
            
            return User(id=user_id, username=username, email=email, phone=phone)
        except Exception as e:
            logging.error(f"USER_DAO: User creation failed - username={username}, error={str(e)}")
            raise
    
    @DecoratorUtils.profile
    def get_user_by_username_or_email(self, username_or_email):
        """Get user by username or email"""
        try:
            query = AuthQueryHelper.get_user_by_username_or_email_query(username_or_email=username_or_email)
            result = self.db_manager.execute_query(query)
            
            if result:
                user = User.from_dict(result[0])
                return user
            return None
        except Exception as e:
            logging.error(f"USER_DAO: Error looking up user - username_or_email={username_or_email}, error={str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            query = AuthQueryHelper.get_user_by_id_query(user_id=user_id)
            result = self.db_manager.execute_query(query)
            
            if result:
                user = User.from_dict(result[0])
                return user
            return None
        except Exception as e:
            logging.error(f"USER_DAO: Error looking up user by ID - user_id={user_id}, error={str(e)}")
            raise


class OTPDAO:
    """Data Access Object for OTP operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    def create_otp(self, user_id):
        """Create a new OTP for the given user"""
        try:
            # First, mark all existing OTPs for this user as used
            self._mark_all_otps_as_used(user_id)
            
            # Generate code
            code = f"{secrets.randbelow(1000000):06d}"
            code = "123456"  # Fixed for development
            
            # Create OTP record using query helper
            expires_at = datetime.now() + timedelta(minutes=5)
            now = datetime.now()
            
            query, values = AuthQueryHelper.create_otp_query(
                user_id=user_id, code=code, expires_at=expires_at, 
                is_used=False, created_at=now
            )
            self.db_manager.execute_insert(query, values)
            
            # Log for development (in production would send via SMS/email)
            DecoratorUtils.highlighted_print(f"*** OTP: {code} for user_id {user_id} ***")
            logging.info(f"OTP_DAO: OTP created - user_id={user_id}, code={code}")
            
            return code
        except Exception as e:
            logging.error(f"OTP_DAO: Error creating OTP - user_id={user_id}, error={str(e)}")
            raise
    
    def _mark_all_otps_as_used(self, user_id):
        """Mark all existing OTPs for a user as used"""
        try:
            # Get count of unused OTPs first
            query = f"SELECT id FROM otps WHERE user_id = {user_id} AND is_used = 0"
            result = self.db_manager.execute_query(query)
            
            if result:
                # Mark all as used using query helper
                update_query = AuthQueryHelper.mark_all_user_otps_as_used_query(user_id=user_id)
                rows_affected = self.db_manager.execute_update(update_query)
                logging.info(f"OTP_DAO: Invalidated {rows_affected} old OTPs for user_id={user_id}")
                
        except Exception as e:
            logging.error(f"OTP_DAO: Error marking OTPs as used - user_id={user_id}, error={str(e)}")
            raise
        
    @DecoratorUtils.profile
    def verify_otp(self, user_id, code):
        """Verify an OTP code"""
        try:
            # Find latest OTP using query helper
            query = AuthQueryHelper.get_latest_unused_otp_query(user_id=user_id, code=code)
            result = self.db_manager.execute_query(query)
            
            if not result:
                logging.warning(f"OTP_DAO: No OTP found - user_id={user_id}, code={code}")
                return False
            
            otp_data = result[0]
            otp = OTP.from_dict(otp_data)
            
            # Check if expired
            current_time = datetime.now()
            if current_time > otp.expires_at:
                logging.warning(f"OTP_DAO: OTP expired - user_id={user_id}, code={code}, expires_at={otp.expires_at}")
                return False
            
            # Mark as used using query helper
            update_query = AuthQueryHelper.mark_otp_as_used_query(otp_id=otp.id)
            self.db_manager.execute_update(update_query)
            logging.info(f"OTP_DAO: OTP verified successfully - user_id={user_id}")
            
            return True
        except Exception as e:
            logging.error(f"OTP_DAO: Error verifying OTP - user_id={user_id}, code={code}, error={str(e)}")
            raise 