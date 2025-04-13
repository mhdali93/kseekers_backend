import time
from fastapi import Query, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from look_up.controller import LookUpController
from logical.jwt_auth import JWTBearer, jwt_auth_required
from logical.logger import log_request, update_log
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, UniversalMessage, ExceptionMessage

import logging

class LookUpRoutes:
    application = app = {}

    def __init__(self):
        self.app = APIRouter()
        self.application = self.app
        self.lu_controller = LookUpController()
        self.__add_routes()

    def __add_routes(self):
        self.app.add_api_route(
            path='/getHeaders',
            endpoint=self.get_headers_info,
            methods=['GET'],
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
