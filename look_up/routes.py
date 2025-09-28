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
        try:
            result = self.lu_controller.get_lookup_types()
            return result
        except Exception as e:
            logging.error(f"LOOKUP_ROUTES: Error getting lookup types - error={str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="Lookup values retrieved successfully",
        error_message="Error retrieving lookup values"
    )
    async def get_lookup_values_by_type(self, request: Request, request_data: LookupValuesByTypeRequest,
                                       logger: str = Query(None, include_in_schema=False)):
        """Get lookup values by type name"""
        try:
            result = self.lu_controller.get_lookup_values_by_type(request_data.type_name)
            return result
        except Exception as e:
            logging.error(f"LOOKUP_ROUTES: Error getting lookup values - type_name={request_data.type_name}, error={str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="Lookup type managed successfully",
        error_message="Error managing lookup type"
    )
    @jwt_auth_required
    async def manage_lookup_type(self, request: Request, type_data: LookupTypeManageRequest,
                                logger: str = Query(None, include_in_schema=False),
                                token: str = Query(None, include_in_schema=False)):
        """Create or update lookup type (upsert by name)"""
        try:
            result = self.lu_controller.manage_lookup_type(type_data.dict())
            logging.info(f"LOOKUP_ROUTES: Lookup type managed - name={type_data.name}")
            return {"name": type_data.name}
        except Exception as e:
            logging.error(f"LOOKUP_ROUTES: Error managing lookup type - name={type_data.name}, error={str(e)}")
            raise
    
    @DecoratorUtils.create_endpoint(
        success_message="Lookup values managed successfully",
        error_message="Error managing lookup values"
    )
    @jwt_auth_required
    async def manage_lookup_values(self, request: Request, request_data: LookupValuesManageRequest,
                                  logger: str = Query(None, include_in_schema=False),
                                  token: str = Query(None, include_in_schema=False)):
        """Create or update lookup values for a type (upsert by code)"""
        try:
            success = self.lu_controller.manage_lookup_values(
                request_data.type_name,
                [value.dict() for value in request_data.values]
            )
            
            if not success:
                logging.error(f"LOOKUP_ROUTES: Failed to manage lookup values - type_name={request_data.type_name}")
                raise HTTPException(status_code=400, detail="Failed to manage lookup values")
            
            logging.info(f"LOOKUP_ROUTES: Lookup values managed - type_name={request_data.type_name}")
            return {"type_name": request_data.type_name, "success": True}
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"LOOKUP_ROUTES: Error managing lookup values - type_name={request_data.type_name}, error={str(e)}")
            raise
        return {"type_name": request_data.type_name}
