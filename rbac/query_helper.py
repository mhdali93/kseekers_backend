import logging

class RBACQueryHelper:
    """Query helper for RBAC-related database operations with module support"""
    
    @staticmethod
    def _convert_boolean_to_int(value):
        """Convert boolean values to integers for database storage"""
        if isinstance(value, bool):
            return 1 if value else 0
        return value
    
    # Role Queries
    @staticmethod
    def create_role_query(name=None, display_name=None, description=None, is_active=None, is_system_role=None, created_at=None, updated_at=None):
        """Returns SQL query for creating a new role with parameterized values"""
        # Validate mandatory fields
        if name is None:
            raise ValueError("name is required for create_role_query")
        if display_name is None:
            raise ValueError("display_name is required for create_role_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['name', 'display_name']
        values = [name, display_name]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if description is not None:
            columns.append('description')
            values.append(description)
        if is_active is not None:
            columns.append('is_active')
            values.append(RBACQueryHelper._convert_boolean_to_int(is_active))
        if is_system_role is not None:
            columns.append('is_system_role')
            values.append(RBACQueryHelper._convert_boolean_to_int(is_system_role))
        if created_at is not None:
            columns.append('created_at')
            values.append(created_at)
        if updated_at is not None:
            columns.append('updated_at')
            values.append(updated_at)
        
        # Create parameterized query
        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join(columns)
        
        query = f"INSERT INTO roles ({columns_str}) VALUES ({placeholders})"
        logging.info(f"RBAC_QUERY_HELPER: Generated query - create_role_query: {query} with values: {values}")
        return query, values
    
    @staticmethod
    def get_role_by_id_query(role_id=None):
        """Returns SQL query for getting role by ID with values formatted"""
        if role_id is None:
            raise ValueError("role_id is required for get_role_by_id_query")
        
        query = f"SELECT * FROM roles WHERE id = {role_id} LIMIT 1"
        logging.info(f"RBAC_QUERY_HELPER: Generated query - get_role_by_id_query: {query}")
        return query
    
    @staticmethod
    def list_roles_query():
        """Returns SQL query for listing roles with filters"""
        query = """
            SELECT * FROM roles 
            WHERE 1=1
        """
        logging.info(f"RBAC_QUERY_HELPER: Generated query - list_roles_query: {query}")
        return query
    
    @staticmethod
    def update_role_query(role_id=None, **kwargs):
        """Returns SQL query for updating role with parameterized values"""
        if role_id is None:
            raise ValueError("role_id is required for update_role_query")
        
        if not kwargs:
            raise ValueError("At least one field must be provided for update")
        
        # Build dynamic set clauses and values
        set_clauses = []
        values = []
        
        # Handle each field in kwargs
        for field, value in kwargs.items():
            if field in ['name', 'display_name', 'description', 'is_active', 'is_system_role']:
                set_clauses.append(f"{field} = %s")
                if field in ['is_active', 'is_system_role']:
                    values.append(RBACQueryHelper._convert_boolean_to_int(value))
                else:
                    values.append(value)
        
        if not set_clauses:
            raise ValueError("No valid fields provided for update")
        
        # Add updated_at
        set_clauses.append("updated_at = %s")
        values.append(kwargs.get('updated_at'))
        
        # Add role_id for WHERE clause
        values.append(role_id)
        
        query = f"UPDATE roles SET {', '.join(set_clauses)} WHERE id = %s"
        logging.info(f"RBAC_QUERY_HELPER: Generated query - update_role_query: {query} with values: {values}")
        return query, values
    
    @staticmethod
    def check_role_name_exists_query(name=None, exclude_id=None):
        """Returns SQL query for checking if role name exists with values formatted"""
        # Validate mandatory fields
        if name is None:
            raise ValueError("name is required for check_role_name_exists_query")
        if exclude_id is None:
            raise ValueError("exclude_id is required for check_role_name_exists_query")
        
        return f"""
            SELECT COUNT(*) as count 
            FROM roles 
            WHERE name = '{name}' AND id != {exclude_id}
        """
    
    # Right Queries
    @staticmethod
    def create_right_query(name=None, display_name=None, description=None, resource_type=None, resource_path=None, http_method=None, module=None, is_active=None, is_system_right=None, created_at=None, updated_at=None):
        """Returns SQL query for creating a new right with parameterized values"""
        # Validate mandatory fields
        if name is None:
            raise ValueError("name is required for create_right_query")
        if display_name is None:
            raise ValueError("display_name is required for create_right_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['name', 'display_name']
        values = [name, display_name]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if description is not None:
            columns.append('description')
            values.append(description)
        if resource_type is not None:
            columns.append('resource_type')
            values.append(resource_type)
        if resource_path is not None:
            columns.append('resource_path')
            values.append(resource_path)
        if http_method is not None:
            columns.append('http_method')
            values.append(http_method)
        if module is not None:
            columns.append('module')
            values.append(module)
        if is_active is not None:
            columns.append('is_active')
            values.append(RBACQueryHelper._convert_boolean_to_int(is_active))
        if is_system_right is not None:
            columns.append('is_system_right')
            values.append(RBACQueryHelper._convert_boolean_to_int(is_system_right))
        if created_at is not None:
            columns.append('created_at')
            values.append(created_at)
        if updated_at is not None:
            columns.append('updated_at')
            values.append(updated_at)
        
        # Create parameterized query
        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join(columns)
        
        query = f"INSERT INTO rights ({columns_str}) VALUES ({placeholders})"
        logging.info(f"RBAC_QUERY_HELPER: Generated query - create_right_query: {query} with values: {values}")
        return query, values
    
    @staticmethod
    def get_right_by_id_query(right_id=None):
        """Returns SQL query for getting right by ID with values formatted"""
        if right_id is None:
            raise ValueError("right_id is required for get_right_by_id_query")
        
        query = f"SELECT * FROM rights WHERE id = {right_id} LIMIT 1"
        logging.info(f"RBAC_QUERY_HELPER: Generated query - get_right_by_id_query: {query}")
        return query
    
    @staticmethod
    def list_rights_query():
        """Returns SQL query for listing rights with filters"""
        query = """
            SELECT * FROM rights 
            WHERE 1=1
        """
        logging.info(f"RBAC_QUERY_HELPER: Generated query - list_rights_query: {query}")
        return query
    
    @staticmethod
    def update_right_query(right_id=None, **kwargs):
        """Returns SQL query for updating right with parameterized values"""
        if right_id is None:
            raise ValueError("right_id is required for update_right_query")
        
        if not kwargs:
            raise ValueError("At least one field must be provided for update")
        
        # Build dynamic set clauses and values
        set_clauses = []
        values = []
        
        # Handle each field in kwargs
        for field, value in kwargs.items():
            if field in ['name', 'display_name', 'description', 'resource_type', 
                       'resource_path', 'http_method', 'module', 'is_active', 'is_system_right']:
                set_clauses.append(f"{field} = %s")
                if field in ['is_active', 'is_system_right']:
                    values.append(RBACQueryHelper._convert_boolean_to_int(value))
                else:
                    values.append(value)
        
        if not set_clauses:
            raise ValueError("No valid fields provided for update")
        
        # Add updated_at
        set_clauses.append("updated_at = %s")
        values.append(kwargs.get('updated_at'))
        
        # Add right_id for WHERE clause
        values.append(right_id)
        
        query = f"UPDATE rights SET {', '.join(set_clauses)} WHERE id = %s"
        logging.info(f"RBAC_QUERY_HELPER: Generated query - update_right_query: {query} with values: {values}")
        return query, values
    
    @staticmethod
    def check_right_name_exists_query(name=None, exclude_id=None):
        """Returns SQL query for checking if right name exists with values formatted"""
        if name is None:
            raise ValueError("name is required for check_right_name_exists_query")
        if exclude_id is None:
            raise ValueError("exclude_id is required for check_right_name_exists_query")
        
        return f"""
            SELECT COUNT(*) as count 
            FROM rights 
            WHERE name = '{name}' AND id != {exclude_id}
        """
    
    # Role-Right Queries
    @staticmethod
    def get_role_rights_with_details_query(role_id=None):
        """Returns SQL query for getting role rights with right details with values formatted"""
        if role_id is None:
            raise ValueError("role_id is required for get_role_rights_with_details_query")
        
        query = f"""
            SELECT 
                rr.id,
                rr.role_id,
                rr.right_id,
                r.name as right_name,
                r.display_name as right_display_name,
                r.description as right_description,
                r.resource_type,
                r.resource_path,
                r.http_method,
                r.module,
                rr.granted_by,
                rr.granted_at,
                rr.is_active,
                rr.created_at
            FROM role_rights rr
            JOIN rights r ON rr.right_id = r.id
            WHERE rr.role_id = {role_id} AND rr.is_active = 1 AND r.is_active = 1
            ORDER BY r.module, r.name
        """
        logging.info(f"RBAC_QUERY_HELPER: Generated query - get_role_rights_with_details_query: {query}")
        return query
    
    @staticmethod
    def get_current_role_rights_query(role_id=None):
        """Returns SQL query for getting current role rights with values formatted"""
        if role_id is None:
            raise ValueError("role_id is required for get_current_role_rights_query")
        
        query = f"""
            SELECT right_id 
            FROM role_rights 
            WHERE role_id = {role_id} AND is_active = 1
        """
        logging.info(f"RBAC_QUERY_HELPER: Generated query - get_current_role_rights_query: {query}")
        return query
    
    @staticmethod
    def add_role_rights_query(role_id=None, right_id=None, granted_by=None, granted_at=None, is_active=None, created_at=None, updated_at=None):
        """Returns SQL query for adding role rights with parameterized values"""
        # Validate mandatory fields
        if role_id is None:
            raise ValueError("role_id is required for add_role_rights_query")
        if right_id is None:
            raise ValueError("right_id is required for add_role_rights_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['role_id', 'right_id']
        values = [role_id, right_id]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if granted_by is not None:
            columns.append('granted_by')
            values.append(granted_by)
        if granted_at is not None:
            columns.append('granted_at')
            values.append(granted_at)
        if is_active is not None:
            columns.append('is_active')
            values.append(RBACQueryHelper._convert_boolean_to_int(is_active))
        if created_at is not None:
            columns.append('created_at')
            values.append(created_at)
        if updated_at is not None:
            columns.append('updated_at')
            values.append(updated_at)
        
        # Create parameterized query
        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join(columns)
        
        query = f"INSERT INTO role_rights ({columns_str}) VALUES ({placeholders})"
        logging.info(f"RBAC_QUERY_HELPER: Generated query - add_role_rights_query: {query} with values: {values}")
        return query, values
    
    @staticmethod
    def remove_role_rights_query(is_active=None, updated_at=None, role_id=None, right_id=None):
        """Returns SQL query for removing role rights with values formatted"""
        # Validate mandatory fields
        if is_active is None:
            raise ValueError("is_active is required for remove_role_rights_query")
        if updated_at is None:
            raise ValueError("updated_at is required for remove_role_rights_query")
        if role_id is None:
            raise ValueError("role_id is required for remove_role_rights_query")
        if right_id is None:
            raise ValueError("right_id is required for remove_role_rights_query")
        
        return f"""
            UPDATE role_rights 
            SET is_active = {is_active}, updated_at = '{updated_at}'
            WHERE role_id = {role_id} AND right_id = {right_id}
        """
    
    # User Rights Queries (using user table role_id field)
    @staticmethod
    def get_user_rights_by_type_query(user_id=None, resource_type=None):
        """Returns SQL query for getting user rights by resource type with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for get_user_rights_by_type_query")
        if resource_type is None:
            raise ValueError("resource_type is required for get_user_rights_by_type_query")
        
        return f"""
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
    
    @staticmethod
    def check_user_api_access_query(user_id=None, resource_path=None):
        """Returns SQL query for checking user API access with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for check_user_api_access_query")
        if resource_path is None:
            raise ValueError("resource_path is required for check_user_api_access_query")
        
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
            LIMIT 1
        """
        logging.info(f"RBAC_QUERY_HELPER: Generated query - check_user_api_access_query: {query}")
        return query
    
    @staticmethod
    def check_user_module_access_query(user_id=None, module=None):
        """Returns SQL query for checking if user has wildcard access to module with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for check_user_module_access_query")
        if module is None:
            raise ValueError("module is required for check_user_module_access_query")
        
        return f"""
            SELECT 
                r.name as right_name,
                r.display_name as right_display_name,
                r.description as right_description
            FROM users u
            JOIN role_rights rr ON u.role_id = rr.role_id
            JOIN rights r ON rr.right_id = r.id
            WHERE u.id = {user_id} 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.module = '{module}'
            AND r.resource_path = '*'
            LIMIT 1
        """
    
    @staticmethod
    def get_user_module_rights_query(user_id=None, module=None):
        """Returns SQL query for getting all user rights for a specific module with values formatted"""
        if user_id is None:
            raise ValueError("user_id is required for get_user_module_rights_query")
        if module is None:
            raise ValueError("module is required for get_user_module_rights_query")
        
        return f"""
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