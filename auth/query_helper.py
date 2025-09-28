import logging

class AuthQueryHelper:
    """Query helper for authentication module - Raw SQL queries"""
    
    @staticmethod
    def _convert_boolean_to_int(value):
        """Convert boolean values to integers for database storage"""
        if isinstance(value, bool):
            return 1 if value else 0
        return value
    
    @staticmethod
    def get_user_by_username_query(username=None):
        """Get SQL query for user by username with values formatted"""
        if username is None:
            raise ValueError("username is required for get_user_by_username_query")
        
        query = f"SELECT * FROM users WHERE username = '{username}' LIMIT 1"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - get_user_by_username_query: {query}")
        return query
    
    @staticmethod
    def get_user_by_email_query(email=None):
        """Get SQL query for user by email with values formatted"""
        if email is None:
            raise ValueError("email is required for get_user_by_email_query")
        
        query = f"SELECT * FROM users WHERE email = '{email}' LIMIT 1"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - get_user_by_email_query: {query}")
        return query
    
    @staticmethod
    def get_user_by_id_query(user_id=None):
        """Get SQL query for user by ID with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for get_user_by_id_query")
        
        query = f"SELECT * FROM users WHERE id = {user_id} LIMIT 1"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - get_user_by_id_query: {query}")
        return query
    
    @staticmethod
    def get_user_by_username_or_email_query(username_or_email=None):
        """Get SQL query for user by username or email with values formatted"""
        if username_or_email is None:
            raise ValueError("username_or_email is required for get_user_by_username_or_email_query")
        
        query = f"SELECT * FROM users WHERE username = '{username_or_email}' OR email = '{username_or_email}' LIMIT 1"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - get_user_by_username_or_email_query: {query}")
        return query
    
    @staticmethod
    def check_existing_user_query(username=None, email=None):
        """Get SQL query to check if user exists by username or email with values formatted"""
        if username is None:
            raise ValueError("username is required for check_existing_user_query")
        if email is None:
            raise ValueError("email is required for check_existing_user_query")
        
        query = f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}' LIMIT 1"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - check_existing_user_query: {query}")
        return query
    
    @staticmethod
    def get_latest_unused_otp_query(user_id=None, code=None):
        """Get SQL query for latest unused OTP for a user with specific code with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for get_latest_unused_otp_query")
        if code is None:
            raise ValueError("code is required for get_latest_unused_otp_query")
        
        query = f"""
            SELECT * FROM otps 
            WHERE user_id = {user_id} AND code = '{code}' AND is_used = 0
            ORDER BY created_at DESC 
            LIMIT 1
        """
        logging.info(f"AUTH_QUERY_HELPER: Generated query - get_latest_unused_otp_query: {query}")
        return query
    
    @staticmethod
    def create_user_query(username=None, email=None, phone=None, is_active=None, is_admin=None, created_at=None, updated_at=None):
        """Get SQL query to create a new user with parameterized values"""
        if username is None:
            raise ValueError("username is required for create_user_query")
        if email is None:
            raise ValueError("email is required for create_user_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['username', 'email']
        values = [username, email]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if phone is not None:
            columns.append('phone')
            values.append(phone)
        if is_active is not None:
            columns.append('is_active')
            values.append(AuthQueryHelper._convert_boolean_to_int(is_active))
        if is_admin is not None:
            columns.append('is_admin')
            values.append(AuthQueryHelper._convert_boolean_to_int(is_admin))
        if created_at is not None:
            columns.append('created_at')
            values.append(created_at)
        if updated_at is not None:
            columns.append('updated_at')
            values.append(updated_at)
        
        # Create parameterized query
        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join(columns)
        
        query = f"INSERT INTO users ({columns_str}) VALUES ({placeholders})"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - create_user_query: {query} with values: {values}")
        return query, values
    
    @staticmethod
    def create_otp_query(user_id=None, code=None, expires_at=None, is_used=None, created_at=None):
        """Get SQL query to create a new OTP with parameterized values"""
        if user_id is None:
            raise ValueError("user_id is required for create_otp_query")
        if code is None:
            raise ValueError("code is required for create_otp_query")
        if expires_at is None:
            raise ValueError("expires_at is required for create_otp_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['user_id', 'code', 'expires_at']
        values = [user_id, code, expires_at]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if is_used is not None:
            columns.append('is_used')
            values.append(AuthQueryHelper._convert_boolean_to_int(is_used))
        if created_at is not None:
            columns.append('created_at')
            values.append(created_at)
        
        # Create parameterized query
        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join(columns)
        
        query = f"INSERT INTO otps ({columns_str}) VALUES ({placeholders})"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - create_otp_query: {query} with values: {values}")
        return query, values
    
    @staticmethod
    def mark_otp_as_used_query(otp_id=None):
        """Get SQL query to mark OTP as used with values formatted"""
        if otp_id is None:
            raise ValueError("otp_id is required for mark_otp_as_used_query")
        
        query = f"UPDATE otps SET is_used = 1 WHERE id = {otp_id}"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - mark_otp_as_used_query: {query}")
        return query
    
    @staticmethod
    def mark_all_user_otps_as_used_query(user_id=None):
        """Get SQL query to mark all OTPs for a user as used with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for mark_all_user_otps_as_used_query")
        
        query = f"UPDATE otps SET is_used = 1 WHERE user_id = {user_id} AND is_used = 0"
        logging.info(f"AUTH_QUERY_HELPER: Generated query - mark_all_user_otps_as_used_query: {query}")
        return query 