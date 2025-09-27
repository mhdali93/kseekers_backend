import time
from fastapi import Query, Depends, APIRouter, Request
from fastapi.encoders import jsonable_encoder
from look_up.controller import LookUpController
from look_up.lookup_schemas import (
    LookupTypeCreate, LookupTypeUpdate, LookupTypeResponse,
    LookupValueCreate, LookupValueUpdate, LookupValueResponse,
    LookupByTypeRequest, LookupValuesByTypeRequest,
    LookupTypeGetRequest, LookupTypeUpdateRequest, LookupTypeDeleteRequest,
    LookupValueGetRequest, LookupValueUpdateRequest, LookupValueDeleteRequest
)
from logical.jwt_auth import JWTBearer, jwt_auth_required
from logical.logger import log_request, update_log
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, UniversalMessage, ExceptionMessage

import logging

class LookUpRoutes:
    application = app = {}

    def __init__(self):
        self.app = APIRouter(prefix="/lookup", tags=["Look Up"])
        self.application = self.app
        self.lu_controller = LookUpController()
        self.__add_routes()

    def __add_routes(self):
        # Legacy endpoint for backward compatibility
        self.app.add_api_route(
            path='/getHeaders',
            endpoint=self.get_headers_info,
            methods=['GET'],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Lookup Types - POST and GET only
        self.app.add_api_route(
            path='/types',
            endpoint=self.get_lookup_types,
            methods=['GET']
        )
        
        self.app.add_api_route(
            path='/types',
            endpoint=self.create_lookup_type,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path='/types/get',
            endpoint=self.get_lookup_type,
            methods=['POST']
        )
        
        self.app.add_api_route(
            path='/types/update',
            endpoint=self.update_lookup_type,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path='/types/delete',
            endpoint=self.delete_lookup_type,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Lookup Values - POST and GET only
        self.app.add_api_route(
            path='/values',
            endpoint=self.get_lookup_values_by_type,
            methods=['POST']
        )
        
        self.app.add_api_route(
            path='/values/create',
            endpoint=self.create_lookup_value,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path='/values/get',
            endpoint=self.get_lookup_value,
            methods=['POST']
        )
        
        self.app.add_api_route(
            path='/values/update',
            endpoint=self.update_lookup_value,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )
        
        self.app.add_api_route(
            path='/values/delete',
            endpoint=self.delete_lookup_value,
            methods=['POST'],
            dependencies=[Depends(JWTBearer())]
        )

    @log_request
    @jwt_auth_required
    async def get_headers_info(self, request: Request,
                               type: str,
                               logger: str = Query(None, include_in_schema=False),
                               token: str = Query(None, include_in_schema=False)):
        start_time = time.time()
        return_json = {}

        try:
            response = self.lu_controller.get_headers_info(type)
            if response:
                logging.info("Got response get_headers_info")
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": response, "error": [], "message": ""},
                    row_count=1,
                    message=""
                )
            else:
                logging.warning('No headers found get_headers_info')
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": ExceptionMessage.headers_not_found.value},
                    row_count=0,
                    message=""
                )
        except Exception as ex:
            logging.error("Inside Exception Block get_headers_info")
            ex_mesg = str(Exception(f"CC_SE_0001: {ex}"))
            logging.error(ex_mesg)
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [], "message": ex_mesg},
                row_count=0,
                message=ex_mesg
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)

        return return_json.get_return_json()
    
    # Lookup Types CRUD endpoints
    @log_request
    async def get_lookup_types(self, request: Request,
                              logger: str = Query(None, include_in_schema=False)):
        """Get all lookup types"""
        start_time = time.time()
        return_json = {}
        
        try:
            types = self.lu_controller.get_lookup_types()
            types_data = [lookup_type.to_dict() for lookup_type in types]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": types_data, "error": [], "message": "Lookup types retrieved successfully"},
                row_count=len(types_data)
            )
        except Exception as e:
            logging.error(f"Get lookup types error: {e}")
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
    async def create_lookup_type(self, request: Request, type_data: LookupTypeCreate,
                                logger: str = Query(None, include_in_schema=False),
                                token: str = Query(None, include_in_schema=False)):
        """Create a new lookup type"""
        start_time = time.time()
        return_json = {}
        
        try:
            lookup_type = self.lu_controller.create_lookup_type(
                type_data.name, type_data.description
            )
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.created,
                rjson={"data": lookup_type.to_dict(), "error": [], "message": "Lookup type created successfully"},
                row_count=1
            )
        except Exception as e:
            logging.error(f"Create lookup type error: {e}")
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
    async def get_lookup_type(self, request: Request, request_data: LookupTypeGetRequest,
                             logger: str = Query(None, include_in_schema=False)):
        """Get lookup type by name"""
        start_time = time.time()
        return_json = {}
        
        try:
            lookup_type = self.lu_controller.get_lookup_type_by_name(request_data.type)
            
            if not lookup_type:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Lookup type not found"},
                    row_count=0
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": lookup_type.to_dict(), "error": [], "message": "Lookup type retrieved successfully"},
                    row_count=1
                )
        except Exception as e:
            logging.error(f"Get lookup type error: {e}")
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
    async def update_lookup_type(self, request: Request, request_data: LookupTypeUpdateRequest,
                                logger: str = Query(None, include_in_schema=False),
                                token: str = Query(None, include_in_schema=False)):
        """Update lookup type"""
        start_time = time.time()
        return_json = {}
        
        try:
            update_data = {k: v for k, v in request_data.dict().items() if v is not None and k != 'type_id'}
            success = self.lu_controller.update_lookup_type(request_data.type_id, **update_data)
            
            if success:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": {"id": request_data.type_id}, "error": [], "message": "Lookup type updated successfully"},
                    row_count=1
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Lookup type not found"},
                    row_count=0
                )
        except Exception as e:
            logging.error(f"Update lookup type error: {e}")
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
    async def delete_lookup_type(self, request: Request, request_data: LookupTypeDeleteRequest,
                                logger: str = Query(None, include_in_schema=False),
                                token: str = Query(None, include_in_schema=False)):
        """Delete lookup type"""
        start_time = time.time()
        return_json = {}
        
        try:
            success = self.lu_controller.delete_lookup_type(request_data.type_id)
            
            if success:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": {"id": request_data.type_id}, "error": [], "message": "Lookup type deleted successfully"},
                    row_count=1
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Lookup type not found"},
                    row_count=0
                )
        except Exception as e:
            logging.error(f"Delete lookup type error: {e}")
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
    
    # Lookup Values CRUD endpoints
    @log_request
    async def get_lookup_values_by_type(self, request: Request, request_data: LookupValuesByTypeRequest,
                                       logger: str = Query(None, include_in_schema=False)):
        """Get lookup values by type name"""
        start_time = time.time()
        return_json = {}
        
        try:
            values = self.lu_controller.get_lookup_values_by_type_name(request_data.lookup_type_name)
            values_data = [value.to_dict() for value in values]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": values_data, "error": [], "message": "Lookup values retrieved successfully"},
                row_count=len(values_data)
            )
        except Exception as e:
            logging.error(f"Get lookup values error: {e}")
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
    async def create_lookup_value(self, request: Request, value_data: LookupValueCreate,
                                 logger: str = Query(None, include_in_schema=False),
                                 token: str = Query(None, include_in_schema=False)):
        """Create a new lookup value"""
        start_time = time.time()
        return_json = {}
        
        try:
            lookup_value = self.lu_controller.create_lookup_value(
                value_data.lookup_type_id, value_data.code, value_data.value,
                value_data.description, value_data.is_active, value_data.sort_order
            )
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.created,
                rjson={"data": lookup_value.to_dict(), "error": [], "message": "Lookup value created successfully"},
                row_count=1
            )
        except Exception as e:
            logging.error(f"Create lookup value error: {e}")
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
    async def get_lookup_value(self, request: Request, request_data: LookupValueGetRequest,
                              logger: str = Query(None, include_in_schema=False)):
        """Get lookup value by ID"""
        start_time = time.time()
        return_json = {}
        
        try:
            lookup_value = self.lu_controller.get_lookup_value_by_id(request_data.value_id)
            
            if not lookup_value:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Lookup value not found"},
                    row_count=0
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": lookup_value.to_dict(), "error": [], "message": "Lookup value retrieved successfully"},
                    row_count=1
                )
        except Exception as e:
            logging.error(f"Get lookup value error: {e}")
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
    async def update_lookup_value(self, request: Request, request_data: LookupValueUpdateRequest,
                                 logger: str = Query(None, include_in_schema=False),
                                 token: str = Query(None, include_in_schema=False)):
        """Update lookup value"""
        start_time = time.time()
        return_json = {}
        
        try:
            update_data = {k: v for k, v in request_data.dict().items() if v is not None and k != 'value_id'}
            success = self.lu_controller.update_lookup_value(request_data.value_id, **update_data)
            
            if success:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": {"id": request_data.value_id}, "error": [], "message": "Lookup value updated successfully"},
                    row_count=1
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Lookup value not found"},
                    row_count=0
                )
        except Exception as e:
            logging.error(f"Update lookup value error: {e}")
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
    async def delete_lookup_value(self, request: Request, request_data: LookupValueDeleteRequest,
                                 logger: str = Query(None, include_in_schema=False),
                                 token: str = Query(None, include_in_schema=False)):
        """Delete lookup value"""
        start_time = time.time()
        return_json = {}
        
        try:
            success = self.lu_controller.delete_lookup_value(request_data.value_id)
            
            if success:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": {"id": request_data.value_id}, "error": [], "message": "Lookup value deleted successfully"},
                    row_count=1
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.not_found,
                    rjson={"data": [], "error": [], "message": "Lookup value not found"},
                    row_count=0
                )
        except Exception as e:
            logging.error(f"Delete lookup value error: {e}")
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
