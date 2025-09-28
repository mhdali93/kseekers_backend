import time
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from utils.decorator import DecoratorUtils

from display_config.display_config_schemas import (
    GridMetadataCreate, GridMetadataUpdate, GridMetadataListRequest, GridMetadataResponse,
    ResultDisplayConfigListRequest, ResultDisplayConfigUpdateRequest, ResultDisplayConfigResponse
)
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, ExceptionMessage
from display_config.controller import DisplayConfigController
from logical.jwt_auth import JWTBearer, jwt_auth_required
from logical.logger import log_request, update_log

import logging

class DisplayConfigRoutes:
    """Display config routes"""
    
    def __init__(self):
        self.app = APIRouter(prefix="/display-config", tags=["Display Config"])
        self.controller = DisplayConfigController()
        self.__add_routes()
    
    def __add_routes(self):
        # Grid Metadata Routes
        self.app.add_api_route(
            path="/grid-metadata/create",
            endpoint=self.create_grid_metadata,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/grid-metadata/list",
            endpoint=self.list_grid_metadata,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/grid-metadata/edit",
            endpoint=self.update_grid_metadata,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Result Display Config Routes
        self.app.add_api_route(
            path="/result-display-config/list",
            endpoint=self.list_display_configs,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/result-display-config/update",
            endpoint=self.update_display_configs,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
    
    # Grid Metadata Endpoints
    @DecoratorUtils.create_endpoint(
        success_message="Grid metadata created successfully",
        error_message=ExceptionMessage.fail_to_create.value,
        success_status=HTTPStatus.created
    )
    @jwt_auth_required
    async def create_grid_metadata(self, request: Request, grid_data: GridMetadataCreate,
                                  logger: str = Query(None, include_in_schema=False),
                                  token: str = Query(None, include_in_schema=False)):
        """Create a new grid metadata"""
        grid_id = self.controller.create_grid_metadata(grid_data.dict())
        return {"id": grid_id}
    
    @DecoratorUtils.create_endpoint(
        success_message="Grid metadata list retrieved successfully",
        error_message="Error retrieving grid metadata list"
    )
    async def list_grid_metadata(self, request: Request, request_data: GridMetadataListRequest,
                                logger: str = Query(None, include_in_schema=False)):
        """List grid metadata with optional filters"""
        return self.controller.list_grid_metadata(
            name=request_data.name,
            is_active=request_data.is_active
        )
    
    @DecoratorUtils.create_endpoint(
        success_message="Grid metadata updated successfully",
        error_message="Error updating grid metadata"
    )
    @jwt_auth_required
    async def update_grid_metadata(self, request: Request, request_data: GridMetadataUpdate,
                                  logger: str = Query(None, include_in_schema=False),
                                  token: str = Query(None, include_in_schema=False)):
        """Update grid metadata"""
        # Filter out None values and id
        update_data = {k: v for k, v in request_data.dict().items() if v is not None and k != 'id'}
        success = self.controller.update_grid_metadata(request_data.id, update_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Grid metadata not found")
        return {"id": request_data.id}
    
    # Result Display Config Endpoints
    @DecoratorUtils.create_endpoint(
        success_message="Display configs retrieved successfully",
        error_message="Error retrieving display configs"
    )
    async def list_display_configs(self, request: Request, request_data: ResultDisplayConfigListRequest,
                                  logger: str = Query(None, include_in_schema=False)):
        """List display configs by gridNameId"""
        return self.controller.list_display_configs(request_data.gridNameId)
    
    @DecoratorUtils.create_endpoint(
        success_message="Display configs updated successfully",
        error_message="Error updating display configs"
    )
    @jwt_auth_required
    async def update_display_configs(self, request: Request, request_data: ResultDisplayConfigUpdateRequest,
                                    logger: str = Query(None, include_in_schema=False),
                                    token: str = Query(None, include_in_schema=False)):
        """Update display configs with upsert logic"""
        success = self.controller.update_display_configs(
            request_data.gridNameId,
            [config.dict() for config in request_data.configs]
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to update display configs")
        return {"gridNameId": request_data.gridNameId}
