import time
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from utils.decorator import DecoratorUtils

from display_config.display_config_schemas import (
    ResultDisplayConfigCreate, ResultDisplayConfigUpdate, ResultDisplayConfigResponse,
    GridHeadersRequest, ResultDisplayConfigByGridRequest, DisplayConfigByIdRequest,
    ResultDisplayConfigListResponse, GridHeadersResponse,
    DisplayConfigGetRequest, DisplayConfigUpdateRequest, DisplayConfigDeleteRequest
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
        self.app.add_api_route(
            path="/grid-headers",
            endpoint=self.get_grid_headers,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/",
            endpoint=self.get_all_display_configs,
            methods=["GET"]
        )
        
        self.app.add_api_route(
            path="/create",
            endpoint=self.create_display_config,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/get",
            endpoint=self.get_display_config,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/update",
            endpoint=self.update_display_config,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/delete",
            endpoint=self.delete_display_config,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path="/by-grid",
            endpoint=self.get_display_configs_by_grid,
            methods=["POST"]
        )
        
        self.app.add_api_route(
            path="/grid-metadata",
            endpoint=self.get_all_grid_metadata,
            methods=["GET"]
        )
    
    @log_request
    async def get_grid_headers(self, request: Request, request_data: GridHeadersRequest,
                              logger: str = Query(None, include_in_schema=False)):
        """Get grid headers by type"""
        start_time = time.time()
        return_json = {}
        
        try:
            headers = self.controller.get_headers_for_grid(request_data.gridNameId)
            
            headers_data = [header.to_dict() for header in headers]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": headers_data, "error": [], "message": "Headers retrieved successfully"},
                row_count=len(headers_data)
            )
        except Exception as e:
            logging.error(f"Get grid headers error: {e}")
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
    async def get_all_display_configs(self, request: Request,
                                     logger: str = Query(None, include_in_schema=False)):
        """Get all display configs"""
        start_time = time.time()
        return_json = {}
        
        try:
            configs = self.controller.get_all_display_configs()
            
            configs_data = [config.to_dict() for config in configs]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": configs_data, "error": [], "message": "Display configs retrieved successfully"},
                row_count=len(configs_data)
            )
        except Exception as e:
            logging.error(f"Get all display configs error: {e}")
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
    async def create_display_config(self, request: Request, config_data: ResultDisplayConfigCreate,
                                   logger: str = Query(None, include_in_schema=False),
                                   token: str = Query(None, include_in_schema=False)):
        """Create a new display config"""
        start_time = time.time()
        return_json = {}
        
        try:
            config_id = self.controller.create_display_config(config_data.dict())
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.created,
                rjson={"data": {"id": config_id}, "error": [], "message": "Display config created successfully"},
                row_count=1
            )
        except ValueError as e:
            logging.error(f"Create display config validation error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            logging.error(f"Create display config error: {e}")
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
    async def get_display_config(self, request: Request, request_data: DisplayConfigGetRequest,
                                logger: str = Query(None, include_in_schema=False)):
        """Get display config by ID"""
        start_time = time.time()
        return_json = {}
        
        try:
            config = self.controller.get_display_config(request_data.config_id)
            
            if not config:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Display config not found"},
                    row_count=0
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": config.to_dict(), "error": [], "message": "Display config retrieved successfully"},
                    row_count=1
                )
        except Exception as e:
            logging.error(f"Get display config error: {e}")
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
    async def update_display_config(self, request: Request, request_data: DisplayConfigUpdateRequest,
                                   logger: str = Query(None, include_in_schema=False),
                                   token: str = Query(None, include_in_schema=False)):
        """Update display config"""
        start_time = time.time()
        return_json = {}
        
        try:
            # Filter out None values and config_id
            update_data = {k: v for k, v in request_data.dict().items() if v is not None and k != 'config_id'}
            
            success = self.controller.update_display_config(request_data.config_id, update_data)
            
            if success:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": {"id": request_data.config_id}, "error": [], "message": "Display config updated successfully"},
                    row_count=1
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Display config not found"},
                    row_count=0
                )
        except ValueError as e:
            logging.error(f"Update display config validation error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            logging.error(f"Update display config error: {e}")
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
    async def delete_display_config(self, request: Request, request_data: DisplayConfigDeleteRequest,
                                   logger: str = Query(None, include_in_schema=False),
                                   token: str = Query(None, include_in_schema=False)):
        """Delete display config"""
        start_time = time.time()
        return_json = {}
        
        try:
            success = self.controller.delete_display_config(request_data.config_id)
            
            if success:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": {"id": request_data.config_id}, "error": [], "message": "Display config deleted successfully"},
                    row_count=1
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Display config not found"},
                    row_count=0
                )
        except ValueError as e:
            logging.error(f"Delete display config validation error: {e}")
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            logging.error(f"Delete display config error: {e}")
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
    async def get_display_configs_by_grid(self, request: Request, request_data: ResultDisplayConfigByGridRequest,
                                         logger: str = Query(None, include_in_schema=False)):
        """Get display configs by grid"""
        start_time = time.time()
        return_json = {}
        
        try:
            configs = self.controller.get_display_configs_by_grid(request_data.gridNameId)
            
            configs_data = [config.to_dict() for config in configs]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": configs_data, "error": [], "message": "Display configs retrieved successfully"},
                row_count=len(configs_data)
            )
        except Exception as e:
            logging.error(f"Get display configs by grid error: {e}")
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
    async def get_all_grid_metadata(self, request: Request,
                                   logger: str = Query(None, include_in_schema=False)):
        """Get all grid metadata"""
        start_time = time.time()
        return_json = {}
        
        try:
            grids = self.controller.get_all_grid_metadata()
            
            grids_data = [grid.to_dict() for grid in grids]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": grids_data, "error": [], "message": "Grid metadata retrieved successfully"},
                row_count=len(grids_data)
            )
        except Exception as e:
            logging.error(f"Get grid metadata error: {e}")
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
