# Simplified RBAC (Role-Based Access Control) Module with Module Support
# This module handles roles, rights, and role-right assignments with simplified APIs
# Users have a single role stored in the user table (no user_roles table)
# Rights belong to modules, and * gives access to entire module

__version__ = "2.1.0"
__author__ = "KSeekers Team"

# Key Features:
# - Users have single role (stored in user.role_id)
# - Email can be duplicate (multiple accounts with different roles)
# - Rights belong to modules
# - Wildcard (*) rights give access to entire module
# - All original fields preserved for audit trails
# - granted_by field maintained for backend auditing

# Simplified API endpoints (GET and POST only):
# 1. POST /rbac/roles - Create role
# 2. GET /rbac/roles - List roles (with name and is_active filters)
# 3. POST /rbac/roles/edit - Edit role (name, display_name, description, is_active)
# 4. POST /rbac/rights - Create right
# 5. GET /rbac/rights - List rights (with name, is_active, and module filters)
# 6. POST /rbac/rights/edit - Edit right (name, display_name, description, is_active, resource_type, resource_path, http_method, module)
# 7. GET /rbac/role-rights/{role_id} - Get all assigned rights for a role
# 8. POST /rbac/role-rights/manage - Manage role rights (add missing, remove extra)
# 9. GET /rbac/user-rights/{user_id} - Get user rights based on resource_type = "ui_page"
# 10. POST /rbac/user-api-access - Check if API is allowed for user