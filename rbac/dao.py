import logging
from datetime import datetime
from manager.db_manager import DBManager
from rbac.rbac_models import Role, Right, RoleRight
from rbac.query_helper import RBACQueryHelper

class RBACDAO:
    """Data Access Object for RBAC operations with module support"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    # Role Operations
    def create_role(self, name, display_name, description=None, is_active=True, is_system_role=False):
        """Create a new role"""
        try:
            query = RBACQueryHelper.create_role_query()
            now = datetime.now()
            role_id = self.db_manager.execute_insert(query, (
                name, display_name, description, is_active, is_system_role, now, now
            ))
            
            return Role(id=role_id, name=name, display_name=display_name, 
                       description=description, is_active=is_active, is_system_role=is_system_role)
        except Exception as e:
            logging.error(f"Error creating role: {e}")
            raise
    
    def get_role_by_id(self, role_id):
        """Get role by ID"""
        try:
            query = RBACQueryHelper.get_role_by_id_query()
            result = self.db_manager.execute_query(query, (role_id,))
            
            if result:
                return Role.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting role by ID {role_id}: {e}")
            raise
    
    def list_roles(self, name=None, is_active=None):
        """List roles with optional filters"""
        try:
            query = RBACQueryHelper.list_roles_query()
            params = []
            
            if name:
                query += " AND name LIKE %s"
                params.append(f"%{name}%")
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            query += " ORDER BY is_system_role DESC, name"
            
            results = self.db_manager.execute_query(query, params)
            return [Role.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error listing roles: {e}")
            raise
    
    def update_role(self, role_id, **kwargs):
        """Update role fields"""
        try:
            if not kwargs:
                return False
            
            set_clauses = []
            params = []
            
            for field, value in kwargs.items():
                if field in ['name', 'display_name', 'description', 'is_active']:
                    set_clauses.append(f"{field} = %s")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            params.append(datetime.now())  # updated_at
            params.append(role_id)         # WHERE id = ?
            
            query = RBACQueryHelper.update_role_query(set_clauses)
            rows_affected = self.db_manager.execute_update(query, params)
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error updating role {role_id}: {e}")
            raise
    
    def check_role_name_exists(self, name, exclude_id=None):
        """Check if role name already exists"""
        try:
            query = RBACQueryHelper.check_role_name_exists_query()
            exclude_id = exclude_id or 0
            result = self.db_manager.execute_query(query, (name, exclude_id))
            
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            logging.error(f"Error checking role name {name}: {e}")
            raise
    
    # Right Operations
    def create_right(self, name, display_name, description=None, resource_type="", 
                    resource_path="", http_method=None, module="default", is_active=True, is_system_right=False):
        """Create a new right"""
        try:
            query = RBACQueryHelper.create_right_query()
            now = datetime.now()
            right_id = self.db_manager.execute_insert(query, (
                name, display_name, description, resource_type, resource_path, 
                http_method, module, is_active, is_system_right, now, now
            ))
            
            return Right(id=right_id, name=name, display_name=display_name, 
                        description=description, resource_type=resource_type, 
                        resource_path=resource_path, http_method=http_method, 
                        module=module, is_active=is_active, is_system_right=is_system_right)
        except Exception as e:
            logging.error(f"Error creating right: {e}")
            raise
    
    def get_right_by_id(self, right_id):
        """Get right by ID"""
        try:
            query = RBACQueryHelper.get_right_by_id_query()
            result = self.db_manager.execute_query(query, (right_id,))
            
            if result:
                return Right.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting right by ID {right_id}: {e}")
            raise
    
    def list_rights(self, name=None, is_active=None, module=None):
        """List rights with optional filters"""
        try:
            query = RBACQueryHelper.list_rights_query()
            params = []
            
            if name:
                query += " AND name LIKE %s"
                params.append(f"%{name}%")
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            if module:
                query += " AND module = %s"
                params.append(module)
            
            query += " ORDER BY module, name"
            
            results = self.db_manager.execute_query(query, params)
            return [Right.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error listing rights: {e}")
            raise
    
    def update_right(self, right_id, **kwargs):
        """Update right fields"""
        try:
            if not kwargs:
                return False
            
            set_clauses = []
            params = []
            
            for field, value in kwargs.items():
                if field in ['name', 'display_name', 'description', 'resource_type', 
                           'resource_path', 'http_method', 'module', 'is_active']:
                    set_clauses.append(f"{field} = %s")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            params.append(datetime.now())  # updated_at
            params.append(right_id)        # WHERE id = ?
            
            query = RBACQueryHelper.update_right_query(set_clauses)
            rows_affected = self.db_manager.execute_update(query, params)
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error updating right {right_id}: {e}")
            raise
    
    def check_right_name_exists(self, name, exclude_id=None):
        """Check if right name already exists"""
        try:
            query = RBACQueryHelper.check_right_name_exists_query()
            exclude_id = exclude_id or 0
            result = self.db_manager.execute_query(query, (name, exclude_id))
            
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            logging.error(f"Error checking right name {name}: {e}")
            raise
    
    # Role-Right Operations
    def get_role_rights_with_details(self, role_id):
        """Get role rights with right details"""
        try:
            query = RBACQueryHelper.get_role_rights_with_details_query()
            results = self.db_manager.execute_query(query, (role_id,))
            
            return [dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting role rights for role {role_id}: {e}")
            raise
    
    def manage_role_rights(self, role_id, right_ids, granted_by=None):
        """Manage role rights - add missing, remove extra"""
        try:
            # Get current role rights
            current_rights_query = RBACQueryHelper.get_current_role_rights_query()
            current_results = self.db_manager.execute_query(current_rights_query, (role_id,))
            current_right_ids = {row['right_id'] for row in current_results}
            
            # Determine what to add and remove
            new_right_ids = set(right_ids)
            to_add = new_right_ids - current_right_ids
            to_remove = current_right_ids - new_right_ids
            
            # Add new rights
            if to_add:
                add_query = RBACQueryHelper.add_role_rights_query()
                now = datetime.now()
                for right_id in to_add:
                    self.db_manager.execute_insert(add_query, (role_id, right_id, granted_by, now, True, now, now))
            
            # Remove old rights
            if to_remove:
                remove_query = RBACQueryHelper.remove_role_rights_query()
                now = datetime.now()
                for right_id in to_remove:
                    self.db_manager.execute_update(remove_query, (False, now, role_id, right_id))
            
            return {
                'added': list(to_add),
                'removed': list(to_remove),
                'total_rights': len(new_right_ids)
            }
        except Exception as e:
            logging.error(f"Error managing role rights for role {role_id}: {e}")
            raise
    
    # User Rights Operations (using user table role_id field)
    def get_user_rights_by_type(self, user_id, resource_type):
        """Get user rights by resource type"""
        try:
            query = RBACQueryHelper.get_user_rights_by_type_query()
            results = self.db_manager.execute_query(query, (user_id, resource_type))
            
            return [dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting user rights by type for user {user_id}: {e}")
            raise
    
    def check_user_api_access(self, user_id, api_path):
        """Check if user has access to specific API path"""
        try:
            query = RBACQueryHelper.check_user_api_access_query()
            results = self.db_manager.execute_query(query, (user_id, api_path))
            
            if results:
                return {
                    'user_id': user_id,
                    'api_path': api_path,
                    'has_access': True,
                    'right_name': results[0]['right_name'],
                    'right_display_name': results[0]['right_display_name'],
                    'right_description': results[0]['right_description'],
                    'module': results[0]['module']
                }
            else:
                return {
                    'user_id': user_id,
                    'api_path': api_path,
                    'has_access': False,
                    'right_name': None,
                    'right_display_name': None,
                    'right_description': None,
                    'module': None
                }
        except Exception as e:
            logging.error(f"Error checking user API access for user {user_id}, path {api_path}: {e}")
            raise
    
    def check_user_module_access(self, user_id, module):
        """Check if user has wildcard access to module"""
        try:
            query = RBACQueryHelper.check_user_module_access_query()
            results = self.db_manager.execute_query(query, (user_id, module))
            
            return len(results) > 0
        except Exception as e:
            logging.error(f"Error checking user module access for user {user_id}, module {module}: {e}")
            raise
    
    def get_user_module_rights(self, user_id, module):
        """Get all user rights for a specific module"""
        try:
            query = RBACQueryHelper.get_user_module_rights_query()
            results = self.db_manager.execute_query(query, (user_id, module))
            
            return [dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting user module rights for user {user_id}, module {module}: {e}")
            raise