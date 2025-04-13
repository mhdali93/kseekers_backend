from sqlmodel import select
from models.auth_models import User, OTP

class AuthQueryHelper:
    """Query helper for authentication module"""
    
    def get_user_by_username_query(self, username):
        """Get query for user by username"""
        return select(User).where(User.username == username)
    
    def get_user_by_email_query(self, email):
        """Get query for user by email"""
        return select(User).where(User.email == email)
    
    def get_user_by_id_query(self, user_id):
        """Get query for user by ID"""
        return select(User).where(User.id == user_id)
    
    def get_user_by_username_or_email_query(self, username_or_email):
        """Get query for user by username or email"""
        if '@' in username_or_email:
            return self.get_user_by_email_query(username_or_email)
        else:
            return self.get_user_by_username_query(username_or_email)
    
    def check_existing_user_query(self, username, email):
        """Get query to check if user exists by username or email"""
        return select(User).where(
            (User.username == username) | (User.email == email)
        )
    
    def get_latest_unused_otp_query(self, user_id, code):
        """Get query for latest unused OTP for a user with specific code"""
        return (
            select(OTP)
            .where(OTP.user_id == user_id, OTP.code == code, OTP.is_used == False)
            .order_by(OTP.created_at.desc())
        ) 