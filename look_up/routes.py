import time
from fastapi import Query, Depends, APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from look_up.controller import LookUpController
from look_up.lookup_schemas import (
    LookupTypeResponse, LookupTypeManageRequest,
    LookupValueResponse, LookupValuesByTypeRequest, LookupValuesManageRequest
)
from logical.jwt_auth import JWTBearer, jwt_auth_required
from logical.logger import log_request, update_log
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, UniversalMessage, ExceptionMessage
from utils.decorator import DecoratorUtils

import logging

class LookUpRoutes:
    application = app = {}

    def __init__(self):
        self.app = APIRouter(prefix="/lookup", tags=["Look Up"])
        self.application = self.app
        self.lu_controller = LookUpController()
        self.__add_routes()

    def __add_routes(self):
        # Simplified Lookup APIs - 4 essential endpoints
        self.app.add_api_route(
            path='/types',
            endpoint=self.get_lookup_types,
            methods=['GET']
        )
        
        self.app.add_api_route(
            path='/values',
            endpoint=self.get_lookup_values_by_type,
            methods=['POST']
        )
        
        self.app.add_api_route(
            path='/types/manage',
            endpoint=self.manage_lookup_type,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path='/values/manage',
            endpoint=self.manage_lookup_values,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )

    # Simplified Lookup API Endpoints
    @DecoratorUtils.create_endpoint(
        success_message="Lookup types retrieved successfully",
        error_message="Error retrieving lookup types"
    )
    async def get_lookup_types(self, request: Request,
                              logger: str = Query(None, include_in_schema=False)):
        """Get all lookup types"""
        return self.lu_controller.get_lookup_types()
    
    @DecoratorUtils.create_endpoint(
        success_message="Lookup values retrieved successfully",
        error_message="Error retrieving lookup values"
    )
    async def get_lookup_values_by_type(self, request: Request, request_data: LookupValuesByTypeRequest,
                                       logger: str = Query(None, include_in_schema=False)):
        """Get lookup values by type name"""
        return self.lu_controller.get_lookup_values_by_type(request_data.type_name)
    
    @DecoratorUtils.create_endpoint(
        success_message="Lookup type managed successfully",
        error_message="Error managing lookup type"
    )
    @jwt_auth_required
    async def manage_lookup_type(self, request: Request, type_data: LookupTypeManageRequest,
                                logger: str = Query(None, include_in_schema=False),
                                token: str = Query(None, include_in_schema=False)):
        """Create or update lookup type (upsert by name)"""
        result = self.lu_controller.manage_lookup_type(type_data.dict())
        return {"name": type_data.name}
    
    @DecoratorUtils.create_endpoint(
        success_message="Lookup values managed successfully",
        error_message="Error managing lookup values"
    )
    @jwt_auth_required
    async def manage_lookup_values(self, request: Request, request_data: LookupValuesManageRequest,
                                  logger: str = Query(None, include_in_schema=False),
                                  token: str = Query(None, include_in_schema=False)):
        """Create or update lookup values for a type (upsert by code)"""
        success = self.lu_controller.manage_lookup_values(
            request_data.type_name,
            [value.dict() for value in request_data.values]
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to manage lookup values")
        return {"type_name": request_data.type_name}
