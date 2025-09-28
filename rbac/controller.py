from fastapi import HTTPException
from rbac.dao import RBACDAO
from rbac.rbac_models import Role, Right, RoleRight

class RBACController:
    """Controller for RBAC business logic with module support"""
    
    def __init__(self):
        self.rbac_dao = RBACDAO()
    
    # Role Business Logic
    def create_role(self, name, display_name, description=None, is_active=True):
        """Create a new role with validation"""
        if not name or len(name.strip()) < 2:
            raise ValueError("Role name must be at least 2 characters")
        
        if not display_name or len(display_name.strip()) < 2:
            raise ValueError("Display name must be at least 2 characters")
        
        if self.rbac_dao.check_role_name_exists(name):
            raise ValueError("Role name already exists")
        
        role = self.rbac_dao.create_role(name, display_name, description, is_active)
        return role.to_dict()
    
    def list_roles(self, name=None, is_active=None):
        """List roles with optional filters"""
        roles = self.rbac_dao.list_roles(name=name, is_active=is_active)
        return [role.to_dict() for role in roles]
    
    def edit_role(self, role_id, **kwargs):
        """Edit role (name, display_name, description, is_active)"""
        if not role_id or role_id <= 0:
            raise ValueError("Invalid role ID")
        
        # Check if role exists
        existing_role = self.rbac_dao.get_role_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        # Check if it's a system role
        if existing_role.is_system_role:
            raise ValueError("Cannot modify system roles")
        
        # Validate update data
        if 'name' in kwargs and kwargs['name']:
            if len(kwargs['name'].strip()) < 2:
                raise ValueError("Role name must be at least 2 characters")
            if self.rbac_dao.check_role_name_exists(kwargs['name'], role_id):
                raise ValueError("Role name already exists")
        
        if 'display_name' in kwargs and kwargs['display_name']:
            if len(kwargs['display_name'].strip()) < 2:
                raise ValueError("Display name must be at least 2 characters")
        
        return self.rbac_dao.update_role(role_id, **kwargs)
    
    # Right Business Logic
    def create_right(self, name, display_name, description=None, resource_type="", 
                    resource_path="", http_method=None, module="default", is_active=True):
        """Create a new right with validation"""
        if not name or len(name.strip()) < 1:
            raise ValueError("Right name must be at least 1 character")
        
        if not display_name or len(display_name.strip()) < 2:
            raise ValueError("Display name must be at least 2 characters")
        
        if not resource_type:
            raise ValueError("Resource type must be provided")
        
        if not resource_path or len(resource_path.strip()) < 1:
            raise ValueError("Resource path must be provided")
        
        if not module or len(module.strip()) < 1:
            raise ValueError("Module must be provided")
        
        if resource_type == 'api_endpoint' and not http_method:
            raise ValueError("HTTP method is required for API endpoint rights")
        
        if self.rbac_dao.check_right_name_exists(name):
            raise ValueError("Right name already exists")
        
        right = self.rbac_dao.create_right(name, display_name, description, resource_type,
                                         resource_path, http_method, module, is_active)
        return right.to_dict()
    
    def list_rights(self, name=None, is_active=None, module=None):
        """List rights with optional filters"""
        rights = self.rbac_dao.list_rights(name=name, is_active=is_active, module=module)
        return [right.to_dict() for right in rights]
    
    def edit_right(self, right_id, **kwargs):
        """Edit right (name, display_name, description, is_active, resource_type, resource_path, http_method, module)"""
        if not right_id or right_id <= 0:
            raise ValueError("Invalid right ID")
        
        # Check if right exists
        existing_right = self.rbac_dao.get_right_by_id(right_id)
        if not existing_right:
            raise HTTPException(status_code=404, detail="Right not found")
        
        # Check if it's a system right
        if existing_right.is_system_right:
            raise ValueError("Cannot modify system rights")
        
        # Validate update data
        if 'name' in kwargs and kwargs['name']:
            if len(kwargs['name'].strip()) < 1:
                raise ValueError("Right name must be at least 1 character")
            if self.rbac_dao.check_right_name_exists(kwargs['name'], right_id):
                raise ValueError("Right name already exists")
        
        if 'display_name' in kwargs and kwargs['display_name']:
            if len(kwargs['display_name'].strip()) < 2:
                raise ValueError("Display name must be at least 2 characters")
        
        if 'resource_type' in kwargs and kwargs['resource_type']:
            if not kwargs['resource_type']:
                raise ValueError("Resource type must be provided")
        
        if 'resource_path' in kwargs and kwargs['resource_path']:
            if len(kwargs['resource_path'].strip()) < 1:
                raise ValueError("Resource path must be provided")
        
        if 'module' in kwargs and kwargs['module']:
            if len(kwargs['module'].strip()) < 1:
                raise ValueError("Module must be provided")
        
        return self.rbac_dao.update_right(right_id, **kwargs)
    
    # Role-Rights Management Business Logic
    def get_role_rights(self, role_id):
        """Get all assigned rights for a role"""
        if not role_id or role_id <= 0:
            raise ValueError("Invalid role ID")
        
        # Check if role exists
        existing_role = self.rbac_dao.get_role_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        role_rights = self.rbac_dao.get_role_rights_with_details(role_id)
        return [role_right for role_right in role_rights]
    
    def manage_role_rights(self, role_id, right_ids, granted_by=None):
        """Manage role rights - add missing, remove extra"""
        if not role_id or role_id <= 0:
            raise ValueError("Invalid role ID")
        
        # Check if role exists
        existing_role = self.rbac_dao.get_role_by_id(role_id)
        if not existing_role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        # Validate all rights exist and are active
        for right_id in right_ids:
            right = self.rbac_dao.get_right_by_id(right_id)
            if not right:
                raise HTTPException(status_code=404, detail=f"Right {right_id} not found")
            if not right.is_active:
                raise ValueError(f"Right {right_id} is not active")
        
        return self.rbac_dao.manage_role_rights(role_id, right_ids, granted_by)
    
    # User Rights Business Logic
    def get_user_ui_rights(self, user_id):
        """Get user rights based on resource_type = 'ui_page'"""
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")
        
        ui_rights = self.rbac_dao.get_user_rights_by_type(user_id, "ui_page")
        return [right for right in ui_rights]
    
    def check_user_api_access(self, user_id, api_path):
        """Check if API is allowed for user"""
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")
        
        if not api_path or len(api_path.strip()) < 1:
            raise ValueError("API path must be provided")
        
        access_info = self.rbac_dao.check_user_api_access(user_id, api_path)
        return access_info
    
    def check_user_module_access(self, user_id, module):
        """Check if user has wildcard access to module"""
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")
        
        if not module or len(module.strip()) < 1:
            raise ValueError("Module must be provided")
        
        return self.rbac_dao.check_user_module_access(user_id, module)
    
    def get_user_module_rights(self, user_id, module):
        """Get all user rights for a specific module"""
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")
        
        if not module or len(module.strip()) < 1:
            raise ValueError("Module must be provided")
        
        return self.rbac_dao.get_user_module_rights(user_id, module)