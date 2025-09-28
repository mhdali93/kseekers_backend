import logging

class UserQueryHelper:
    """Query helper for user module - Raw SQL queries"""
    
    @staticmethod
    def _convert_boolean_to_int(value):
        """Convert boolean values to integers for database storage"""
        if isinstance(value, bool):
            return 1 if value else 0
        return value
    
    # User CRUD Queries
    @staticmethod
    def get_user_by_id_query(user_id=None):
        """Get SQL query for user by ID with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for get_user_by_id_query")
        
        query = f"SELECT * FROM users WHERE id = {user_id} LIMIT 1"
        logging.info(f"USER_QUERY_HELPER: Generated query - get_user_by_id_query: {query}")
        return query
    
    @staticmethod
    def get_user_by_username_query(username=None):
        """Get SQL query for user by username with values formatted"""
        if username is None:
            raise ValueError("username is required for get_user_by_username_query")
        
        query = f"SELECT * FROM users WHERE username = '{username}' LIMIT 1"
        logging.info(f"USER_QUERY_HELPER: Generated query - get_user_by_username_query: {query}")
        return query
    
    @staticmethod
    def get_user_by_email_query(email=None):
        """Get SQL query for user by email with values formatted"""
        if email is None:
            raise ValueError("email is required for get_user_by_email_query")
        
        query = f"SELECT * FROM users WHERE email = '{email}' LIMIT 1"
        logging.info(f"USER_QUERY_HELPER: Generated query - get_user_by_email_query: {query}")
        return query
    
    @staticmethod
    def get_user_by_username_or_email_query(username_or_email=None):
        """Get SQL query for user by username or email with values formatted"""
        if username_or_email is None:
            raise ValueError("username_or_email is required for get_user_by_username_or_email_query")
        
        query = f"SELECT * FROM users WHERE username = '{username_or_email}' OR email = '{username_or_email}' LIMIT 1"
        logging.info(f"USER_QUERY_HELPER: Generated query - get_user_by_username_or_email_query: {query}")
        return query
    
    @staticmethod
    def list_users_query(page=1, per_page=10, search=None, is_active=None, role_id=None):
        """Get SQL query for listing users with pagination and filters"""
        offset = (page - 1) * per_page
        
        query = "SELECT * FROM users WHERE 1=1"
        
        if search:
            query += f" AND (username LIKE '%{search}%' OR email LIKE '%{search}%')"
        
        if is_active is not None:
            query += f" AND is_active = {UserQueryHelper._convert_boolean_to_int(is_active)}"
        
        if role_id is not None:
            query += f" AND role_id = {role_id}"
        
        query += f" ORDER BY created_at DESC LIMIT {per_page} OFFSET {offset}"
        logging.info(f"USER_QUERY_HELPER: Generated query - list_users_query: {query}")
        return query
    
    @staticmethod
    def count_users_query(search=None, is_active=None, role_id=None):
        """Get SQL query for counting users with filters"""
        query = "SELECT COUNT(*) as total FROM users WHERE 1=1"
        
        if search:
            query += f" AND (username LIKE '%{search}%' OR email LIKE '%{search}%')"
        
        if is_active is not None:
            query += f" AND is_active = {UserQueryHelper._convert_boolean_to_int(is_active)}"
        
        if role_id is not None:
            query += f" AND role_id = {role_id}"
        
        logging.info(f"USER_QUERY_HELPER: Generated query - count_users_query: {query}")
        return query
    
    @staticmethod
    def create_user_query(username=None, email=None, phone=None, is_active=None, is_admin=None, role_id=None, created_at=None, updated_at=None):
        """Get SQL query to create a new user with values directly bound"""
        if username is None:
            raise ValueError("username is required for create_user_query")
        if email is None:
            raise ValueError("email is required for create_user_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['username', 'email']
        values = [f"'{username}'", f"'{email}'"]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if phone is not None:
            columns.append('phone')
            values.append(f"'{phone}'")
        if is_active is not None:
            columns.append('is_active')
            values.append(str(UserQueryHelper._convert_boolean_to_int(is_active)))
        if is_admin is not None:
            columns.append('is_admin')
            values.append(str(UserQueryHelper._convert_boolean_to_int(is_admin)))
        if role_id is not None:
            columns.append('role_id')
            values.append(str(role_id))
        if created_at is not None:
            columns.append('created_at')
            values.append(f"'{created_at}'")
        if updated_at is not None:
            columns.append('updated_at')
            values.append(f"'{updated_at}'")
        
        # Create query with values directly bound
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        
        query = f"INSERT INTO users ({columns_str}) VALUES ({values_str})"
        logging.info(f"USER_QUERY_HELPER: Generated query - create_user_query: {query}")
        return query
    
    @staticmethod
    def update_user_query(user_id=None, username=None, email=None, phone=None, is_active=None, is_admin=None, role_id=None, updated_at=None):
        """Get SQL query to update a user with values directly bound"""
        if user_id is None:
            raise ValueError("user_id is required for update_user_query")
        
        # Build dynamic set clauses with values directly bound
        set_clauses = []
        
        if username is not None:
            set_clauses.append(f"username = '{username}'")
        if email is not None:
            set_clauses.append(f"email = '{email}'")
        if phone is not None:
            set_clauses.append(f"phone = '{phone}'")
        if is_active is not None:
            set_clauses.append(f"is_active = {UserQueryHelper._convert_boolean_to_int(is_active)}")
        if is_admin is not None:
            set_clauses.append(f"is_admin = {UserQueryHelper._convert_boolean_to_int(is_admin)}")
        if role_id is not None:
            set_clauses.append(f"role_id = {role_id}")
        if updated_at is not None:
            set_clauses.append(f"updated_at = '{updated_at}'")
        
        if not set_clauses:
            raise ValueError("At least one field must be provided for update")
        
        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = {user_id}"
        logging.info(f"USER_QUERY_HELPER: Generated query - update_user_query: {query}")
        return query
    
    @staticmethod
    def check_user_exists_query(username=None, email=None, exclude_id=None):
        """Get SQL query to check if user exists by username or email with values formatted"""
        if username is None and email is None:
            raise ValueError("username or email is required for check_user_exists_query")
        
        query = "SELECT * FROM users WHERE ("
        conditions = []
        
        if username:
            conditions.append(f"username = '{username}'")
        if email:
            conditions.append(f"email = '{email}'")
        
        query += " OR ".join(conditions)
        
        if exclude_id:
            query += f") AND id != {exclude_id}"
        else:
            query += ")"
        
        query += " LIMIT 1"
        logging.info(f"USER_QUERY_HELPER: Generated query - check_user_exists_query: {query}")
        return query
    
    # User Rights Queries (moved from RBAC)
    @staticmethod
    def get_user_rights_by_type_query(user_id=None, resource_type=None):
        """Get SQL query for getting user rights by resource type with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for get_user_rights_by_type_query")
        if resource_type is None:
            raise ValueError("resource_type is required for get_user_rights_by_type_query")
        
        query = f"""
            SELECT DISTINCT
                r.id,
                r.name,
                r.display_name,
                r.description,
                r.resource_type,
                r.resource_path,
                r.http_method,
                r.module
            FROM users u
            JOIN role_rights rr ON u.role_id = rr.role_id
            JOIN rights r ON rr.right_id = r.id
            WHERE u.id = {user_id} 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.resource_type = '{resource_type}'
            ORDER BY r.module, r.name
        """
        logging.info(f"USER_QUERY_HELPER: Generated query - get_user_rights_by_type_query: {query}")
        return query
    
    @staticmethod
    def check_user_api_access_query(user_id=None, resource_path=None, http_method=None):
        """Get SQL query for checking user API access with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for check_user_api_access_query")
        if resource_path is None:
            raise ValueError("resource_path is required for check_user_api_access_query")
        
        method_condition = ""
        if http_method:
            method_condition = f"AND (r.http_method = '{http_method}' OR r.http_method = '*')"
        
        query = f"""
            SELECT 
                r.name as right_name,
                r.display_name as right_display_name,
                r.description as right_description,
                r.module
            FROM users u
            JOIN role_rights rr ON u.role_id = rr.role_id
            JOIN rights r ON rr.right_id = r.id
            WHERE u.id = {user_id} 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.resource_type = 'api_endpoint'
            AND (r.resource_path = '{resource_path}' OR r.resource_path = '*')
            {method_condition}
            LIMIT 1
        """
        logging.info(f"USER_QUERY_HELPER: Generated query - check_user_api_access_query: {query}")
        return query
    
    @staticmethod
    def get_user_module_rights_query(user_id=None, module=None):
        """Get SQL query for getting all user rights for a specific module with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for get_user_module_rights_query")
        if module is None:
            raise ValueError("module is required for get_user_module_rights_query")
        
        query = f"""
            SELECT DISTINCT
                r.id,
                r.name,
                r.display_name,
                r.description,
                r.resource_type,
                r.resource_path,
                r.http_method,
                r.module
            FROM users u
            JOIN role_rights rr ON u.role_id = rr.role_id
            JOIN rights r ON rr.right_id = r.id
            WHERE u.id = {user_id} 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.module = '{module}'
            ORDER BY r.name
        """
        logging.info(f"USER_QUERY_HELPER: Generated query - get_user_module_rights_query: {query}")
        return query
