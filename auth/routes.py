import time
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from utils.decorator import DecoratorUtils

from auth.auth_schemas import (
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
    
    @DecoratorUtils.create_endpoint(
        success_message="User created successfully",
        error_message=ExceptionMessage.fail_to_create.value,
        success_status=HTTPStatus.created
    )
    # @jwt_auth_required
    async def register_user(self, request: Request, user_data: UserCreate,
                           logger: str = Query(None, include_in_schema=False)):
        """Register a new user"""
        user = self.controller.register_user(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone
        )
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "is_admin": user.is_admin
        }
    
    @DecoratorUtils.create_endpoint(
        success_message="OTP sent successfully",
        error_message="Error requesting OTP"
    )
    async def request_otp(self, request: Request, request_data: OTPRequest,
                         logger: str = Query(None, include_in_schema=False)):
        """Request an OTP"""
        # Find user
        user = self.controller.get_user(request_data.username_or_email)
        if not user:
            raise HTTPException(status_code=404, detail=ExceptionMessage.member_not_found.value)
        
        # Generate OTP
        self.controller.generate_otp(user.id)
        return {"email": user.email}
    
    @DecoratorUtils.create_endpoint(
        success_message=UniversalMessage.access_token.value,
        error_message="Error verifying OTP"
    )
    async def verify_otp(self, request: Request, verify: OTPVerify,
                        logger: str = Query(None, include_in_schema=False)):
        """Verify OTP and get token"""
        # Get token using the login method
        token = self.controller.login(verify.username_or_email, verify.otp_code)
        return {"access_token": token, "token_type": "bearer"}
    
    @DecoratorUtils.create_endpoint(
        success_message="User profile retrieved successfully",
        error_message="Error retrieving user profile"
    )
    @jwt_auth_required
    async def get_current_user(self, request: Request,
                              logger: str = Query(None, include_in_schema=False),
                              token: str = Query(None, include_in_schema=False)):
        """Get current user profile"""
        user_id = request.state.user_id
        user = self.controller.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail=ExceptionMessage.member_not_found.value)
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "is_admin": user.is_admin
        } 