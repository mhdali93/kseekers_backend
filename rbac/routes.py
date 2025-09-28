import time
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from utils.decorator import DecoratorUtils
from logical.logger import log_request, update_log
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, ExceptionMessage
from rbac.controller import RBACController
from rbac.rbac_schemas import (
    RoleCreate, RoleUpdate, RoleListRequest,
    RightCreate, RightUpdate, RightListRequest,
    RoleRightsRequest, RoleRightsManageRequest,
    UserRightsRequest, UserApiAccessRequest
)
from logical.jwt_auth import JWTBearer, jwt_auth_required

class RBACRoutes:
    """Simplified RBAC API routes with module support"""
    
    def __init__(self):
        self.app = APIRouter(prefix="/rbac", tags=["RBAC"])
        self.controller = RBACController()
        self.__add_routes()
    
    def __add_routes(self):
        # 1. Role Management Routes
        self.app.add_api_route(
            path="/roles",
            endpoint=self.create_role,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/roles",
            endpoint=self.list_roles,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/roles/edit",
            endpoint=self.edit_role,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # 4. Right Management Routes
        self.app.add_api_route(
            path="/rights",
            endpoint=self.create_right,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/rights",
            endpoint=self.list_rights,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/rights/edit",
            endpoint=self.edit_right,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # 7. Role-Rights Management Routes
        self.app.add_api_route(
            path="/role-rights/{role_id}",
            endpoint=self.get_role_rights,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/role-rights/manage",
            endpoint=self.manage_role_rights,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # 9. Misc Routes
        self.app.add_api_route(
            path="/user-rights/{user_id}",
            endpoint=self.get_user_ui_rights,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/user-api-access",
            endpoint=self.check_user_api_access,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
    
    # 1. Role Management Endpoints
    @DecoratorUtils.create_endpoint(
        success_message="Role created successfully",
        error_message=ExceptionMessage.fail_to_create.value,
        success_status=HTTPStatus.created
    )
    @jwt_auth_required
    async def create_role(self, request: Request, role_data: RoleCreate,
                          token: str = Query(None, include_in_schema=False),
                          logger: str = Query(None, include_in_schema=False)):
        """Create a new role"""
        return self.controller.create_role(
            name=role_data.name,
            display_name=role_data.display_name,
            description=role_data.description,
            is_active=role_data.is_active
        )
    
    @DecoratorUtils.create_endpoint(
        success_message="Roles retrieved successfully",
        error_message="Error retrieving roles"
    )
    @jwt_auth_required
    async def list_roles(self, request: Request, name: str = Query(None), 
                        is_active: bool = Query(None),
                        token: str = Query(None, include_in_schema=False),
                        logger: str = Query(None, include_in_schema=False)):
        """List roles with optional name and is_active filters"""
        return self.controller.list_roles(name=name, is_active=is_active)
    
    @DecoratorUtils.create_endpoint(
        success_message="Role updated successfully",
        error_message="Error updating role"
    )
    @jwt_auth_required
    async def edit_role(self, request: Request, role_data: RoleUpdate, 
                       token: str = Query(None, include_in_schema=False),
                       logger: str = Query(None, include_in_schema=False)):
        """Edit role (name, display_name, description, is_active)"""
        role_id = role_data.id
        update_data = {k: v for k, v in role_data.dict().items() if k != 'id' and v is not None}
        return self.controller.edit_role(role_id, **update_data)
    
    # 4. Right Management Endpoints
    @DecoratorUtils.create_endpoint(
        success_message="Right created successfully",
        error_message=ExceptionMessage.fail_to_create.value,
        success_status=HTTPStatus.created
    )
    @jwt_auth_required
    async def create_right(self, request: Request, right_data: RightCreate,
                          token: str = Query(None, include_in_schema=False),
                          logger: str = Query(None, include_in_schema=False)):
        """Create a new right"""
        return self.controller.create_right(
            name=right_data.name,
            display_name=right_data.display_name,
            description=right_data.description,
            resource_type=right_data.resource_type,
            resource_path=right_data.resource_path,
            http_method=right_data.http_method,
            module=right_data.module,
            is_active=right_data.is_active
        )
    
    @DecoratorUtils.create_endpoint(
        success_message="Rights retrieved successfully",
        error_message="Error retrieving rights"
    )
    @jwt_auth_required
    async def list_rights(self, request: Request, name: str = Query(None), 
                         is_active: bool = Query(None), module: str = Query(None),
                         token: str = Query(None, include_in_schema=False),
                         logger: str = Query(None, include_in_schema=False)):
        """List rights with optional name, is_active, and module filters"""
        return self.controller.list_rights(name=name, is_active=is_active, module=module)
    
    @DecoratorUtils.create_endpoint(
        success_message="Right updated successfully",
        error_message="Error updating right"
    )
    @jwt_auth_required
    async def edit_right(self, request: Request, right_data: RightUpdate, 
                        token: str = Query(None, include_in_schema=False),
                        logger: str = Query(None, include_in_schema=False)):
        """Edit right (name, display_name, description, is_active, resource_type, resource_path, http_method, module)"""
        right_id = right_data.id
        update_data = {k: v for k, v in right_data.dict().items() if k != 'id' and v is not None}
        return self.controller.edit_right(right_id, **update_data)
    
    # 7. Role-Rights Management Endpoints
    @DecoratorUtils.create_endpoint(
        success_message="Role rights retrieved successfully",
        error_message="Error retrieving role rights"
    )
    @jwt_auth_required
    async def get_role_rights(self, request: Request, role_id: int,
                             token: str = Query(None, include_in_schema=False),
                             logger: str = Query(None, include_in_schema=False)):
        """Get all assigned rights for a role"""
        return self.controller.get_role_rights(role_id)
    
    @DecoratorUtils.create_endpoint(
        success_message="Role rights updated successfully",
        error_message="Error updating role rights"
    )
    @jwt_auth_required
    async def manage_role_rights(self, request: Request, 
                                rights_data: RoleRightsManageRequest,
                                token: str = Query(None, include_in_schema=False),
                                logger: str = Query(None, include_in_schema=False)):
        """Manage role rights - add missing, remove extra"""
        # Extract granted_by from request state (set by JWT authentication)
        granted_by = getattr(request.state, "user_id", None)
        return self.controller.manage_role_rights(rights_data.role_id, rights_data.right_ids, granted_by)
    
    # 9. Misc Endpoints
    @DecoratorUtils.create_endpoint(
        success_message="User UI rights retrieved successfully",
        error_message="Error retrieving user UI rights"
    )
    @jwt_auth_required
    async def get_user_ui_rights(self, request: Request, user_id: int,
                                token: str = Query(None, include_in_schema=False),
                                logger: str = Query(None, include_in_schema=False)):
        """Get user rights based on resource_type = 'ui_page'"""
        return self.controller.get_user_ui_rights(user_id)
    
    @DecoratorUtils.create_endpoint(
        success_message="User API access checked successfully",
        error_message="Error checking user API access"
    )
    @jwt_auth_required
    async def check_user_api_access(self, request: Request, access_data: UserApiAccessRequest, 
                                   token: str = Query(None, include_in_schema=False),
                                   logger: str = Query(None, include_in_schema=False)):
        """Check if API is allowed for user"""
        return self.controller.check_user_api_access(access_data.user_id, access_data.api_path)