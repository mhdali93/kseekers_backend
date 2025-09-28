from fastapi import APIRouter, HTTPException, Depends, Request, Query
from typing import List, Optional
from utils.decorator import DecoratorUtils

from users.user_schemas import (
    UserCreate, UserUpdate, UserResponse, UserListResponse,
    UserRightsResponse, UserApiAccessRequest, UserApiAccessResponse,
    RightResponse, RoleResponse, MessageResponse
)
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, ExceptionMessage, UniversalMessage
from users.controller import UserController
from logical.jwt_auth import JWTBearer, jwt_auth_required
from logical.logger import log_request, update_log

import logging


class UserRoutes:
    """User management routes"""
    
    def __init__(self):
        self.app = APIRouter(prefix="/users", tags=["User Management"])
        self.controller = UserController()
        self.__add_routes()
    
    def __add_routes(self):
        # User CRUD endpoints - clear and descriptive paths
        self.app.add_api_route(
            path="/list",
            endpoint=self.list_users,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/create",
            endpoint=self.create_user,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/get/{user_id}",
            endpoint=self.get_user,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/update",
            endpoint=self.update_user,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # User rights endpoints
        self.app.add_api_route(
            path="/rights/{user_id}",
            endpoint=self.get_user_rights,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/api-access",
            endpoint=self.check_user_api_access,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
    
    @DecoratorUtils.create_endpoint(
        success_message="Users retrieved successfully",
        error_message="Error retrieving users"
    )
    @jwt_auth_required
    async def list_users(self, request: Request,
                        page: int = Query(1, ge=1, description="Page number"),
                        per_page: int = Query(10, ge=1, le=100, description="Items per page"),
                        search: Optional[str] = Query(None, description="Search term"),
                        is_active: Optional[bool] = Query(None, description="Filter by active status"),
                        role_id: Optional[int] = Query(None, description="Filter by role ID"),
                        logger: str = Query(None, include_in_schema=False)):
        """List users with pagination and filters"""
        try:
            users, total = self.controller.list_users(page, per_page, search, is_active, role_id)
            
            user_responses = [UserResponse(**user.to_dict()) for user in users]
            
            return UserListResponse(
                users=user_responses,
                total=total,
                page=page,
                per_page=per_page
            )
        except Exception as e:
            logging.error(f"USER_ROUTES: Error listing users - error: {str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="User created successfully",
        error_message=ExceptionMessage.fail_to_create.value,
        success_status=HTTPStatus.created
    )
    @jwt_auth_required
    async def create_user(self, request: Request, user_data: UserCreate,
                         logger: str = Query(None, include_in_schema=False)):
        """Create a new user (moved from auth/register)"""
        try:
            user = self.controller.create_user(user_data)
            return UserResponse(**user.to_dict())
        except HTTPException as e:
            logging.error(f"USER_ROUTES: User creation failed - status={e.status_code}, detail={e.detail}")
            raise
        except Exception as e:
            logging.error(f"USER_ROUTES: User creation failed - error: {str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="User retrieved successfully",
        error_message="Error retrieving user"
    )
    @jwt_auth_required
    async def get_user(self, request: Request, user_id: int,
                      logger: str = Query(None, include_in_schema=False)):
        """Get user by ID"""
        try:
            user = self.controller.get_user(user_id)
            return UserResponse(**user.to_dict())
        except HTTPException as e:
            logging.error(f"USER_ROUTES: User retrieval failed - status={e.status_code}, detail={e.detail}")
            raise
        except Exception as e:
            logging.error(f"USER_ROUTES: User retrieval failed - error: {str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="User updated successfully",
        error_message="Error updating user"
    )
    @jwt_auth_required
    async def update_user(self, request: Request, user_data: UserUpdate,
                         logger: str = Query(None, include_in_schema=False)):
        """Update a user"""
        try:
            user = self.controller.update_user(user_data.user_id, user_data)
            return UserResponse(**user.to_dict())
        except HTTPException as e:
            logging.error(f"USER_ROUTES: User update failed - status={e.status_code}, detail={e.detail}")
            raise
        except Exception as e:
            logging.error(f"USER_ROUTES: User update failed - error: {str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="User rights retrieved successfully",
        error_message="Error retrieving user rights"
    )
    @jwt_auth_required
    async def get_user_rights(self, request: Request, user_id: int,
                             resource_type: Optional[str] = Query(None, description="Filter by resource type"),
                             module: Optional[str] = Query(None, description="Filter by module"),
                             logger: str = Query(None, include_in_schema=False)):
        """Get user rights (inherited through user's role) - moved from rbac/user-rights/{user_id}"""
        try:
            # First get the user to get username and role info
            user = self.controller.get_user(user_id)
            
            # Get user rights (inherited through role)
            rights = self.controller.get_user_rights(user_id, resource_type, module)
            
            right_responses = []
            for right in rights:
                right_responses.append(RightResponse(
                    id=right.id,
                    name=right.name,
                    display_name=right.display_name,
                    description=right.description,
                    resource_type=right.resource_type,
                    resource_path=right.resource_path,
                    http_method=right.http_method,
                    module=right.module,
                    is_active=right.is_active
                ))
            
            return UserRightsResponse(
                user_id=user.id,
                username=user.username,
                role_id=user.role_id,
                role_name=None,  # Could be populated if needed
                rights=right_responses
            )
        except HTTPException as e:
            logging.error(f"USER_ROUTES: User rights retrieval failed - status={e.status_code}, detail={e.detail}")
            raise
        except Exception as e:
            logging.error(f"USER_ROUTES: User rights retrieval failed - error: {str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="API access checked successfully",
        error_message="Error checking API access"
    )
    @jwt_auth_required
    async def check_user_api_access(self, request: Request, 
                                   access_request: UserApiAccessRequest,
                                   logger: str = Query(None, include_in_schema=False)):
        """Check user API access (moved from rbac)"""
        try:
            result = self.controller.check_user_api_access(access_request.user_id, access_request)
            return UserApiAccessResponse(**result)
        except HTTPException as e:
            logging.error(f"USER_ROUTES: API access check failed - status={e.status_code}, detail={e.detail}")
            raise
        except Exception as e:
            logging.error(f"USER_ROUTES: API access check failed - error: {str(e)}")
            raise
