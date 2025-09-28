class RBACQueryHelper:
    """Query helper for RBAC-related database operations with module support"""
    
    # Role Queries
    @staticmethod
    def create_role_query():
        """Returns SQL query for creating a new role"""
        return """
            INSERT INTO roles (name, display_name, description, is_active, is_system_role, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def get_role_by_id_query():
        """Returns SQL query for getting role by ID"""
        return "SELECT * FROM roles WHERE id = %s LIMIT 1"
    
    @staticmethod
    def list_roles_query():
        """Returns SQL query for listing roles with filters"""
        return """
            SELECT * FROM roles 
            WHERE 1=1
        """
    
    @staticmethod
    def update_role_query(set_clauses):
        """Returns SQL query for updating role"""
        return f"""
            UPDATE roles 
            SET {', '.join(set_clauses)}, updated_at = %s
            WHERE id = %s
        """
    
    @staticmethod
    def check_role_name_exists_query():
        """Returns SQL query for checking if role name exists"""
        return """
            SELECT COUNT(*) as count 
            FROM roles 
            WHERE name = %s AND id != %s
        """
    
    # Right Queries
    @staticmethod
    def create_right_query():
        """Returns SQL query for creating a new right"""
        return """
            INSERT INTO rights (name, display_name, description, resource_type, resource_path, http_method, module, is_active, is_system_right, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def get_right_by_id_query():
        """Returns SQL query for getting right by ID"""
        return "SELECT * FROM rights WHERE id = %s LIMIT 1"
    
    @staticmethod
    def list_rights_query():
        """Returns SQL query for listing rights with filters"""
        return """
            SELECT * FROM rights 
            WHERE 1=1
        """
    
    @staticmethod
    def update_right_query(set_clauses):
        """Returns SQL query for updating right"""
        return f"""
            UPDATE rights 
            SET {', '.join(set_clauses)}, updated_at = %s
            WHERE id = %s
        """
    
    @staticmethod
    def check_right_name_exists_query():
        """Returns SQL query for checking if right name exists"""
        return """
            SELECT COUNT(*) as count 
            FROM rights 
            WHERE name = %s AND id != %s
        """
    
    # Role-Right Queries
    @staticmethod
    def get_role_rights_with_details_query():
        """Returns SQL query for getting role rights with right details"""
        return """
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
            WHERE rr.role_id = %s AND rr.is_active = 1 AND r.is_active = 1
            ORDER BY r.module, r.name
        """
    
    @staticmethod
    def get_current_role_rights_query():
        """Returns SQL query for getting current role rights"""
        return """
            SELECT right_id 
            FROM role_rights 
            WHERE role_id = %s AND is_active = 1
        """
    
    @staticmethod
    def add_role_rights_query():
        """Returns SQL query for adding role rights"""
        return """
            INSERT INTO role_rights (role_id, right_id, granted_by, granted_at, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def remove_role_rights_query():
        """Returns SQL query for removing role rights"""
        return """
            UPDATE role_rights 
            SET is_active = %s, updated_at = %s
            WHERE role_id = %s AND right_id = %s
        """
    
    # User Rights Queries (using user table role_id field)
    @staticmethod
    def get_user_rights_by_type_query():
        """Returns SQL query for getting user rights by resource type"""
        return """
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
            WHERE u.id = %s 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.resource_type = %s
            ORDER BY r.module, r.name
        """
    
    @staticmethod
    def check_user_api_access_query():
        """Returns SQL query for checking user API access"""
        return """
            SELECT 
                r.name as right_name,
                r.display_name as right_display_name,
                r.description as right_description,
                r.module
            FROM users u
            JOIN role_rights rr ON u.role_id = rr.role_id
            JOIN rights r ON rr.right_id = r.id
            WHERE u.id = %s 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.resource_type = 'api_endpoint'
            AND (r.resource_path = %s OR r.resource_path = '*')
            LIMIT 1
        """
    
    @staticmethod
    def check_user_module_access_query():
        """Returns SQL query for checking if user has wildcard access to module"""
        return """
            SELECT 
                r.name as right_name,
                r.display_name as right_display_name,
                r.description as right_description
            FROM users u
            JOIN role_rights rr ON u.role_id = rr.role_id
            JOIN rights r ON rr.right_id = r.id
            WHERE u.id = %s 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.module = %s
            AND r.resource_path = '*'
            LIMIT 1
        """
    
    @staticmethod
    def get_user_module_rights_query():
        """Returns SQL query for getting all user rights for a specific module"""
        return """
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
            WHERE u.id = %s 
            AND u.role_id IS NOT NULL
            AND rr.is_active = 1 
            AND r.is_active = 1
            AND r.module = %s
            ORDER BY r.name
        """