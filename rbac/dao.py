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
    def create_role(self, name, display_name, description=None, is_system_role=False):
        """Create a new role"""
        try:
            now = datetime.now()
            query = RBACQueryHelper.create_role_query(
                name=name, display_name=display_name, description=description, 
                is_active=1, is_system_role=is_system_role, 
                created_at=now, updated_at=now
            )
            role_id = self.db_manager.execute_insert(query)
            
            return Role(id=role_id, name=name, display_name=display_name, 
                       description=description or "", is_active=1, is_system_role=is_system_role)
        except Exception as e:
            logging.error(f"RBAC_DAO: Role creation failed - name={name}, error={str(e)}")
            raise
    
    def get_role_by_id(self, role_id):
        """Get role by ID"""
        try:
            query = RBACQueryHelper.get_role_by_id_query(role_id=role_id)
            result = self.db_manager.execute_query(query)
            
            if result:
                return Role.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"RBAC_DAO: Error getting role by ID - role_id={role_id}, error={str(e)}")
            raise
    
    def list_roles(self, name=None, is_active=None):
        """List roles with optional filters"""
        try:
            query = RBACQueryHelper.list_roles_query()
            
            if name:
                query += f" AND name LIKE '%{name}%'"
            
            if is_active is not None:
                query += f" AND is_active = {RBACQueryHelper._convert_boolean_to_int(is_active)}"
            
            query += " ORDER BY is_system_role DESC, name"
            
            results = self.db_manager.execute_query(query)
            return [Role.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"RBAC_DAO: Error listing roles - error={str(e)}")
            raise
    
    def update_role(self, role_id, **kwargs):
        """Update role fields"""
        try:
            if not kwargs:
                return False
            
            updated_at = datetime.now()
            kwargs['updated_at'] = updated_at
            
            query = RBACQueryHelper.update_role_query(
                role_id=role_id, 
                **kwargs
            )
            rows_affected = self.db_manager.execute_update(query)
            return rows_affected > 0
        except Exception as e:
            logging.error(f"RBAC_DAO: Error updating role - role_id={role_id}, error={str(e)}")
            raise
    
    def check_role_name_exists(self, name, exclude_id=None):
        """Check if role name already exists"""
        try:
            exclude_id = exclude_id or 0
            query = RBACQueryHelper.check_role_name_exists_query(name=name, exclude_id=exclude_id)
            result = self.db_manager.execute_query(query)
            
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            logging.error(f"RBAC_DAO: Error checking role name - name={name}, error={str(e)}")
            raise
    
    # Right Operations
    def create_right(self, name, display_name, description=None, resource_type="", 
                    resource_path="", http_method=None, module="default", is_system_right=False):
        """Create a new right"""
        try:
            now = datetime.now()
            query = RBACQueryHelper.create_right_query(
                name=name, display_name=display_name, description=description, 
                resource_type=resource_type, resource_path=resource_path, 
                http_method=http_method, module=module, is_active=1, 
                is_system_right=is_system_right, created_at=now, updated_at=now
            )
            right_id = self.db_manager.execute_insert(query)
            
            return Right(id=right_id, name=name, display_name=display_name, 
                        description=description or "", resource_type=resource_type, 
                        resource_path=resource_path, http_method=http_method, 
                        module=module, is_active=1, is_system_right=is_system_right)
        except Exception as e:
            logging.error(f"RBAC_DAO: Right creation failed - name={name}, error={str(e)}")
            raise
    
    def get_right_by_id(self, right_id):
        """Get right by ID"""
        try:
            query = RBACQueryHelper.get_right_by_id_query(right_id=right_id)
            result = self.db_manager.execute_query(query)
            
            if result:
                return Right.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"RBAC_DAO: Error getting right by ID - right_id={right_id}, error={str(e)}")
            raise
    
    def list_rights(self, name=None, is_active=None, module=None):
        """List rights with optional filters"""
        try:
            query = RBACQueryHelper.list_rights_query()
            
            if name:
                query += f" AND name LIKE '%{name}%'"
            
            if is_active is not None:
                query += f" AND is_active = {RBACQueryHelper._convert_boolean_to_int(is_active)}"
            
            if module:
                query += f" AND module = '{module}'"
            
            query += " ORDER BY module, name"
            
            results = self.db_manager.execute_query(query)
            return [Right.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"RBAC_DAO: Error listing rights - error={str(e)}")
            raise
    
    def update_right(self, right_id, **kwargs):
        """Update right fields"""
        try:
            if not kwargs:
                return False
            
            updated_at = datetime.now()
            kwargs['updated_at'] = updated_at
            
            query = RBACQueryHelper.update_right_query(
                right_id=right_id, 
                **kwargs
            )
            rows_affected = self.db_manager.execute_update(query)
            return rows_affected > 0
        except Exception as e:
            logging.error(f"RBAC_DAO: Error updating right - right_id={right_id}, error={str(e)}")
            raise
    
    def check_right_name_exists(self, name, exclude_id=None):
        """Check if right name already exists"""
        try:
            exclude_id = exclude_id or 0
            query = RBACQueryHelper.check_right_name_exists_query(name=name, exclude_id=exclude_id)
            result = self.db_manager.execute_query(query)
            
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            logging.error(f"RBAC_DAO: Error checking right name - name={name}, error={str(e)}")
            raise
    
    # Role-Right Operations
    def get_role_rights_with_details(self, role_id):
        """Get role rights with right details"""
        try:
            query = RBACQueryHelper.get_role_rights_with_details_query(role_id=role_id)
            results = self.db_manager.execute_query(query)
            
            return [dict(row) for row in results]
        except Exception as e:
            logging.error(f"RBAC_DAO: Error getting role rights - role_id={role_id}, error={str(e)}")
            raise
    
    def manage_role_rights(self, role_id, right_ids, granted_by=None):
        """Manage role rights - add missing, remove extra"""
        try:
            # Get current role rights
            current_rights_query = RBACQueryHelper.get_current_role_rights_query(role_id=role_id)
            current_results = self.db_manager.execute_query(current_rights_query)
            current_right_ids = {row['right_id'] for row in current_results}
            
            # Determine what to add and remove
            new_right_ids = set(right_ids)
            to_add = new_right_ids - current_right_ids
            to_remove = current_right_ids - new_right_ids
            
            # Add new rights
            if to_add:
                now = datetime.now()
                for right_id in to_add:
                    add_query = RBACQueryHelper.add_role_rights_query(
                        role_id=role_id, right_id=right_id, granted_by=granted_by, 
                        granted_at=now, is_active=True, created_at=now, updated_at=now
                    )
                    self.db_manager.execute_insert(add_query)
            
            # Remove old rights
            if to_remove:
                now = datetime.now()
                for right_id in to_remove:
                    remove_query = RBACQueryHelper.remove_role_rights_query(
                        is_active=False, updated_at=now, role_id=role_id, right_id=right_id
                    )
                    self.db_manager.execute_update(remove_query)
            
            return {
                'added': list(to_add),
                'removed': list(to_remove),
                'total_rights': len(new_right_ids)
            }
        except Exception as e:
            logging.error(f"RBAC_DAO: Error managing role rights - role_id={role_id}, error={str(e)}")
            raise
    
    # User Rights Operations (using user table role_id field)
    def get_user_rights_by_type(self, user_id, resource_type):
        """Get user rights by resource type"""
        try:
            query = RBACQueryHelper.get_user_rights_by_type_query(user_id=user_id, resource_type=resource_type)
            results = self.db_manager.execute_query(query)
            
            return [dict(row) for row in results]
        except Exception as e:
            logging.error(f"RBAC_DAO: Error getting user rights by type - user_id={user_id}, error={str(e)}")
            raise
    
    def check_user_api_access(self, user_id, api_path):
        """Check if user has access to specific API path"""
        try:
            query = RBACQueryHelper.check_user_api_access_query(user_id=user_id, resource_path=api_path)
            results = self.db_manager.execute_query(query)
            
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
            logging.error(f"RBAC_DAO: Error checking user API access - user_id={user_id}, path={api_path}, error={str(e)}")
            raise
    
    def check_user_module_access(self, user_id, module):
        """Check if user has wildcard access to module"""
        try:
            query = RBACQueryHelper.check_user_module_access_query(user_id=user_id, module=module)
            results = self.db_manager.execute_query(query)
            
            return len(results) > 0
        except Exception as e:
            logging.error(f"RBAC_DAO: Error checking user module access - user_id={user_id}, module={module}, error={str(e)}")
            raise
    
    def get_user_module_rights(self, user_id, module):
        """Get all user rights for a specific module"""
        try:
            query = RBACQueryHelper.get_user_module_rights_query(user_id=user_id, module=module)
            results = self.db_manager.execute_query(query)
            
            return [dict(row) for row in results]
        except Exception as e:
            logging.error(f"RBAC_DAO: Error getting user module rights - user_id={user_id}, module={module}, error={str(e)}")
            raise