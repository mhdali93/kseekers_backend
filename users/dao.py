import logging
from typing import List, Optional, Tuple
from datetime import datetime

from manager.db_manager import DBManager
from users.user_models import User
from rbac.rbac_models import Right, Role
from users.query_helper import UserQueryHelper


class UserDAO:
    """Data Access Object for user operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
        self.query_helper = UserQueryHelper()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            query = self.query_helper.get_user_by_id_query(user_id)
            result = self.db_manager.execute_query(query)
            
            if result and len(result) > 0:
                row = result[0]
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row.get('phone'),
                    is_active=bool(row.get('is_active', 1)),
                    is_admin=bool(row.get('is_admin', 0)),
                    role_id=row.get('role_id'),
                    created_at=row.get('created_at'),
                    updated_at=row.get('updated_at')
                )
            return None
        except Exception as e:
            logging.error(f"USER_DAO: Error getting user by ID - user_id={user_id}, error={str(e)}")
            raise
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            query = self.query_helper.get_user_by_username_query(username)
            result = self.db_manager.execute_query(query)
            
            if result and len(result) > 0:
                row = result[0]
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row.get('phone'),
                    is_active=bool(row.get('is_active', 1)),
                    is_admin=bool(row.get('is_admin', 0)),
                    role_id=row.get('role_id'),
                    created_at=row.get('created_at'),
                    updated_at=row.get('updated_at')
                )
            return None
        except Exception as e:
            logging.error(f"USER_DAO: Error getting user by username - username={username}, error={str(e)}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            query = self.query_helper.get_user_by_email_query(email)
            result = self.db_manager.execute_query(query)
            
            if result and len(result) > 0:
                row = result[0]
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row.get('phone'),
                    is_active=bool(row.get('is_active', 1)),
                    is_admin=bool(row.get('is_admin', 0)),
                    role_id=row.get('role_id'),
                    created_at=row.get('created_at'),
                    updated_at=row.get('updated_at')
                )
            return None
        except Exception as e:
            logging.error(f"USER_DAO: Error getting user by email - email={email}, error={str(e)}")
            raise
    
    def get_user_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        """Get user by username or email"""
        try:
            query = self.query_helper.get_user_by_username_or_email_query(username_or_email)
            result = self.db_manager.execute_query(query)
            
            if result and len(result) > 0:
                row = result[0]
                return User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row.get('phone'),
                    is_active=bool(row.get('is_active', 1)),
                    is_admin=bool(row.get('is_admin', 0)),
                    role_id=row.get('role_id'),
                    created_at=row.get('created_at'),
                    updated_at=row.get('updated_at')
                )
            return None
        except Exception as e:
            logging.error(f"USER_DAO: Error getting user by username or email - username_or_email={username_or_email}, error={str(e)}")
            raise
    
    def list_users(self, page: int = 1, per_page: int = 10, search: str = None, 
                   is_active: bool = None, role_id: int = None) -> Tuple[List[User], int]:
        """List users with pagination and filters"""
        try:
            # Get users
            query, params = self.query_helper.list_users_query(page, per_page, search, is_active, role_id)
            result = self.db_manager.execute_query(query, params)
            
            users = []
            if result:
                for row in result:
                    users.append(User(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        phone=row.get('phone'),
                        is_active=bool(row.get('is_active', 1)),
                        is_admin=bool(row.get('is_admin', 0)),
                        role_id=row.get('role_id'),
                        created_at=row.get('created_at'),
                        updated_at=row.get('updated_at')
                    ))
            
            # Get total count
            count_query, count_params = self.query_helper.count_users_query(search, is_active, role_id)
            count_result = self.db_manager.execute_query(count_query, count_params)
            total = count_result[0]['total'] if count_result else 0
            
            return users, total
        except Exception as e:
            logging.error(f"USER_DAO: Error listing users - page={page}, per_page={per_page}, error={str(e)}")
            raise
    
    def create_user(self, username: str, email: str, phone: str = None, 
                   is_active: bool = True, is_admin: bool = False, role_id: int = None) -> User:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = self.get_user_by_username_or_email(username)
            if existing_user:
                raise ValueError("User with this username or email already exists")
            
            # Create user
            query = self.query_helper.create_user_query(
                username=username,
                email=email,
                phone=phone,
                is_active=is_active,
                is_admin=is_admin,
                role_id=role_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            user_id = self.db_manager.execute_insert(query)
            
            # Return the created user
            return self.get_user_by_id(user_id)
        except Exception as e:
            logging.error(f"USER_DAO: Error creating user - username={username}, email={email}, error={str(e)}")
            raise
    
    def update_user(self, user_id: int, username: str = None, email: str = None, 
                   phone: str = None, is_active: bool = None, is_admin: bool = None, 
                   role_id: int = None) -> User:
        """Update a user"""
        try:
            # Check if user exists
            existing_user = self.get_user_by_id(user_id)
            if not existing_user:
                raise ValueError("User not found")
            
            # Check for conflicts if username or email is being updated
            if username or email:
                check_query = self.query_helper.check_user_exists_query(
                    username=username or existing_user.username,
                    email=email or existing_user.email,
                    exclude_id=user_id
                )
                conflict_result = self.db_manager.execute_query(check_query)
                if conflict_result:
                    raise ValueError("User with this username or email already exists")
            
            # Update user
            query = self.query_helper.update_user_query(
                user_id=user_id,
                username=username,
                email=email,
                phone=phone,
                is_active=is_active,
                is_admin=is_admin,
                role_id=role_id,
                updated_at=datetime.now()
            )
            
            self.db_manager.execute_update(query)
            
            # Return the updated user
            return self.get_user_by_id(user_id)
        except Exception as e:
            logging.error(f"USER_DAO: Error updating user - user_id={user_id}, error={str(e)}")
            raise
    
    def get_user_rights_by_type(self, user_id: int, resource_type: str) -> List[Right]:
        """Get user rights by resource type (inherited through user's role)"""
        try:
            query = self.query_helper.get_user_rights_by_type_query(user_id, resource_type)
            result = self.db_manager.execute_query(query)
            
            rights = []
            if result:
                for row in result:
                    rights.append(Right(
                        id=row['id'],
                        name=row['name'],
                        display_name=row['display_name'],
                        description=row.get('description'),
                        resource_type=row.get('resource_type'),
                        resource_path=row.get('resource_path'),
                        http_method=row.get('http_method'),
                        module=row.get('module'),
                        is_active=bool(row.get('is_active', 1))
                    ))
            
            return rights
        except Exception as e:
            logging.error(f"USER_DAO: Error getting user rights by type - user_id={user_id}, resource_type={resource_type}, error={str(e)}")
            raise
    
    def check_user_api_access(self, user_id: int, resource_path: str, http_method: str = "GET") -> Optional[Right]:
        """Check if user has API access (inherited through user's role)"""
        try:
            query = self.query_helper.check_user_api_access_query(user_id, resource_path, http_method)
            result = self.db_manager.execute_query(query)
            
            if result and len(result) > 0:
                row = result[0]
                return Right(
                    id=0,  # Not needed for this use case
                    name=row['right_name'],
                    display_name=row['right_display_name'],
                    description=row.get('right_description'),
                    resource_type='api_endpoint',
                    resource_path=resource_path,
                    http_method=http_method,
                    module=row.get('module'),
                    is_active=True
                )
            return None
        except Exception as e:
            logging.error(f"USER_DAO: Error checking user API access - user_id={user_id}, resource_path={resource_path}, error={str(e)}")
            raise
    
    def get_user_module_rights(self, user_id: int, module: str) -> List[Right]:
        """Get all user rights for a specific module (inherited through user's role)"""
        try:
            query = self.query_helper.get_user_module_rights_query(user_id, module)
            result = self.db_manager.execute_query(query)
            
            rights = []
            if result:
                for row in result:
                    rights.append(Right(
                        id=row['id'],
                        name=row['name'],
                        display_name=row['display_name'],
                        description=row.get('description'),
                        resource_type=row.get('resource_type'),
                        resource_path=row.get('resource_path'),
                        http_method=row.get('http_method'),
                        module=row.get('module'),
                        is_active=bool(row.get('is_active', 1))
                    ))
            
            return rights
        except Exception as e:
            logging.error(f"USER_DAO: Error getting user module rights - user_id={user_id}, module={module}, error={str(e)}")
            raise
