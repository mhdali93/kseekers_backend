class AuthQueryHelper:
    """Query helper for authentication module - Raw SQL queries"""
    
    @staticmethod
    def get_user_by_username_query():
        """Get SQL query for user by username"""
        return "SELECT * FROM users WHERE username = %s LIMIT 1"
    
    @staticmethod
    def get_user_by_email_query():
        """Get SQL query for user by email"""
        return "SELECT * FROM users WHERE email = %s LIMIT 1"
    
    @staticmethod
    def get_user_by_id_query():
        """Get SQL query for user by ID"""
        return "SELECT * FROM users WHERE id = %s LIMIT 1"
    
    @staticmethod
    def get_user_by_username_or_email_query():
        """Get SQL query for user by username or email"""
        return "SELECT * FROM users WHERE username = %s OR email = %s LIMIT 1"
    
    @staticmethod
    def check_existing_user_query():
        """Get SQL query to check if user exists by username or email"""
        return "SELECT * FROM users WHERE username = %s OR email = %s LIMIT 1"
    
    @staticmethod
    def get_latest_unused_otp_query():
        """Get SQL query for latest unused OTP for a user with specific code"""
        return """
            SELECT * FROM otps 
            WHERE user_id = %s AND code = %s AND is_used = 0
            ORDER BY created_at DESC 
            LIMIT 1
        """
    
    @staticmethod
    def create_user_query():
        """Get SQL query to create a new user"""
        return """
            INSERT INTO users (username, email, phone, is_active, is_admin, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def create_otp_query():
        """Get SQL query to create a new OTP"""
        return """
            INSERT INTO otps (user_id, code, expires_at, is_used, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def mark_otp_as_used_query():
        """Get SQL query to mark OTP as used"""
        return "UPDATE otps SET is_used = 1 WHERE id = %s" 