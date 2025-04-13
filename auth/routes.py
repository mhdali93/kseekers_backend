import time
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from utils.decorator import DecoratorUtils

from models.auth_schemas import (
    UserCreate, UserResponse, TokenResponse,
    OTPRequest, OTPVerify, MessageResponse
)
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, ExceptionMessage, UniversalMessage
from auth.controller import AuthController
from logical.jwt_auth import JWTBearer, jwt_auth_required
from logical.logger import log_request, update_log

import logging

class AuthRoutes:
    """Authentication routes"""
    
    def __init__(self):
        self.app = APIRouter(prefix="/auth", tags=["Authentication"])
        self.controller = AuthController()
        self.__add_routes()
    
    def __add_routes(self):
        self.app.add_api_route(
            path="/register",
            endpoint=self.register_user,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/otp/request",
            endpoint=self.request_otp,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/otp/verify",
            endpoint=self.verify_otp,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/me",
            endpoint=self.get_current_user,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
    
    @log_request
    async def register_user(self, request: Request, user_data: UserCreate,
                           logger: str = Query(None, include_in_schema=False)):
        """Register a new user"""
        start_time = time.time()
        return_json = {}
        
        try:
            user = self.controller.register_user(
                username=user_data.username,
                email=user_data.email,
                phone=user_data.phone
            )
            
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "is_admin": user.is_admin
            }
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.created,
                rjson={"data": user_data, "error": [], "message": "User created successfully"},
                row_count=1
            )
        except ValueError as e:
            logging.error(f"Register user error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.conflict,
                rjson={"data": [], "error": [str(e)], "message": ExceptionMessage.duplicate_name_entry.value},
                row_count=0
            )
        except Exception as e:
            logging.error(f"Register user error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": ExceptionMessage.fail_to_create.value},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @DecoratorUtils.profile
    async def request_otp(self, request: Request, request_data: OTPRequest,
                         logger: str = Query(None, include_in_schema=False)):
        """Request an OTP"""
        start_time = time.time()
        return_json = {}
        
        try:
            # Find user
            user = self.controller.get_user(request_data.username_or_email)
            if not user:
                logging.warning('User not found for OTP request')
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": ExceptionMessage.member_not_found.value},
                    row_count=0
                )
            else:
                # Generate OTP
                self.controller.generate_otp(user.id)
                
                logging.info(f"OTP generated for user: {user.email}")
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": {"email": user.email}, "error": [], "message": "OTP sent successfully"},
                    row_count=1
                )
        except Exception as e:
            logging.error(f"OTP request error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": ExceptionMessage.fail_to_create.value},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    async def verify_otp(self, request: Request, verify: OTPVerify,
                        logger: str = Query(None, include_in_schema=False)):
        """Verify OTP and get token"""
        start_time = time.time()
        return_json = {}
        
        try:
            # Get token using the login method
            token = self.controller.login(verify.username_or_email, verify.otp_code)
            
            logging.info(f"OTP verified for user: {verify.username_or_email}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": {"access_token": token, "token_type": "bearer"}, "error": [], "message": UniversalMessage.access_token.value},
                row_count=1
            )
        except HTTPException as e:
            logging.error(f"OTP verification error: {e.detail}")
            status_code = HTTPStatus.unauthorized if e.status_code == 401 else \
                          HTTPStatus.not_found if e.status_code == 404 else \
                          HTTPStatus.error
            
            return_json = ReturnJson(
                status_and_code=status_code,
                rjson={"data": [], "error": [str(e.detail)], "message": e.detail},
                row_count=0
            )
        except Exception as e:
            logging.error(f"OTP verification error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": ExceptionMessage.fail_to_create.value},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @jwt_auth_required
    async def get_current_user(self, request: Request,
                              logger: str = Query(None, include_in_schema=False),
                              token: str = Query(None, include_in_schema=False)):
        """Get current user profile"""
        start_time = time.time()
        return_json = {}
        
        try:
            user_id = request.state.user_id
            user = self.controller.get_user_by_id(user_id)
            
            if not user:
                logging.warning(f"User not found: {user_id}")
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": ExceptionMessage.member_not_found.value},
                    row_count=0
                )
            else:
                logging.info(f"User profile retrieved: {user.username}")
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "is_admin": user.is_admin
                }
                
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": user_data, "error": [], "message": ""},
                    row_count=1
                )
        except HTTPException as e:
            logging.error(f"Get user error: {e.detail}")
            status_code = HTTPStatus.unauthorized if e.status_code == 401 else \
                          HTTPStatus.not_found if e.status_code == 404 else \
                          HTTPStatus.error
            
            return_json = ReturnJson(
                status_and_code=status_code,
                rjson={"data": [], "error": [str(e.detail)], "message": e.detail},
                row_count=0
            )
        except Exception as e:
            logging.error(f"Get user error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": ExceptionMessage.fail_to_create.value},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json() 