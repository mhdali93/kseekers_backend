from fastapi import HTTPException
import logging
from typing import List, Tuple, Optional

from users.user_models import User
from rbac.rbac_models import Right, Role
from users.dao import UserDAO
from users.user_schemas import UserCreate, UserUpdate, UserApiAccessRequest


class UserController:
    """Controller for user business logic"""
    
    def __init__(self):
        self.user_dao = UserDAO()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            user = self.user_dao.create_user(
                username=user_data.username,
                email=user_data.email,
                phone=user_data.phone,
                is_active=user_data.is_active,
                is_admin=user_data.is_admin,
                role_id=user_data.role_id
            )
            logging.info(f"USER_CONTROLLER: User created successfully - user_id={user.id}, username={user.username}")
            return user
        except ValueError as e:
            logging.warning(f"USER_CONTROLLER: User creation failed - {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logging.error(f"USER_CONTROLLER: User creation failed - error={str(e)}")
            raise
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID"""
        try:
            user = self.user_dao.get_user_by_id(user_id)
            if not user:
                logging.warning(f"USER_CONTROLLER: User not found - user_id={user_id}")
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"USER_CONTROLLER: Error getting user - user_id={user_id}, error={str(e)}")
            raise
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update a user"""
        try:
            # Convert Pydantic model to dict, excluding None values
            update_data = user_data.dict(exclude_unset=True)
            
            user = self.user_dao.update_user(
                user_id=user_id,
                username=update_data.get('username'),
                email=update_data.get('email'),
                phone=update_data.get('phone'),
                is_active=update_data.get('is_active'),
                is_admin=update_data.get('is_admin'),
                role_id=update_data.get('role_id')
            )
            logging.info(f"USER_CONTROLLER: User updated successfully - user_id={user_id}")
            return user
        except ValueError as e:
            logging.warning(f"USER_CONTROLLER: User update failed - {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logging.error(f"USER_CONTROLLER: User update failed - user_id={user_id}, error={str(e)}")
            raise
    
    def list_users(self, page: int = 1, per_page: int = 10, search: str = None, 
                  is_active: bool = None, role_id: int = None) -> Tuple[List[User], int]:
        """List users with pagination and filters"""
        try:
            users, total = self.user_dao.list_users(page, per_page, search, is_active, role_id)
            logging.info(f"USER_CONTROLLER: Listed users - page={page}, per_page={per_page}, total={total}")
            return users, total
        except Exception as e:
            logging.error(f"USER_CONTROLLER: Error listing users - error={str(e)}")
            raise
    
    def get_user_rights(self, user_id: int, resource_type: str = None, module: str = None) -> List[Right]:
        """Get user rights by type or module (inherited through user's role)"""
        try:
            if resource_type:
                rights = self.user_dao.get_user_rights_by_type(user_id, resource_type)
            elif module:
                rights = self.user_dao.get_user_module_rights(user_id, module)
            else:
                # Get all rights (both api_endpoint and other types)
                api_rights = self.user_dao.get_user_rights_by_type(user_id, 'api_endpoint')
                other_rights = self.user_dao.get_user_rights_by_type(user_id, 'other')
                rights = api_rights + other_rights
            
            logging.info(f"USER_CONTROLLER: Retrieved user rights - user_id={user_id}, count={len(rights)}")
            return rights
        except Exception as e:
            logging.error(f"USER_CONTROLLER: Error getting user rights - user_id={user_id}, error={str(e)}")
            raise
    
    def check_user_api_access(self, user_id: int, access_request: UserApiAccessRequest) -> dict:
        """Check if user has API access"""
        try:
            right = self.user_dao.check_user_api_access(
                user_id=user_id,
                resource_path=access_request.resource_path,
                http_method=access_request.http_method
            )
            
            has_access = right is not None
            result = {
                "has_access": has_access,
                "right_name": right.name if right else None,
                "right_display_name": right.display_name if right else None,
                "module": right.module if right else None
            }
            
            logging.info(f"USER_CONTROLLER: Checked API access - user_id={user_id}, has_access={has_access}")
            return result
        except Exception as e:
            logging.error(f"USER_CONTROLLER: Error checking API access - user_id={user_id}, error={str(e)}")
            raise
