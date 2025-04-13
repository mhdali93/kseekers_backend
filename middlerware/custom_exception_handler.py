import time
import traceback

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from models.enums import HTTPStatus
from models.enums import TypeOfErrorEnum, UniversalMessage
from models.result import Result
from models.returnjson import ReturnJson


# Define a custom exception handler middleware
class CustomExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            res = Result()
            start_time = time.time()
            response = await call_next(request)
            if response.status_code == 403:
                error_message = UniversalMessage.permission_denied.value
                start_time = time.time()
                res.result_obj = {"data": {},
                                  "error": [],
                                  "message": error_message
                                  }
                res.result_code = HTTPStatus.bad_request
                end_time = time.time()
                rtn = res.get()
                returnJson = ReturnJson(end_time - start_time, rtn['code'], rtn['object'], rtn['message'])
                returnJson.http_status = HTTPStatus.bad_request.value[0]

                return returnJson.get_return_json()
            return response

        except Exception as e:
            traceback.print_exc()
            # Handle other exceptions
            error_message = UniversalMessage.some_thing_went_wrong.value
            start_time = time.time()
            res.result_obj = {"data": {},
                              "error": [],
                              "message": error_message
                              }
            res.result_code = HTTPStatus.error
            end_time = time.time()
            rtn = res.get()
            returnJson = ReturnJson(end_time - start_time, rtn['code'], rtn['object'], rtn['message'])
            returnJson.http_status = HTTPStatus.bad_request.value[0]
            return returnJson.get_return_json()


class RequestValidationExceptionHandler:
    @staticmethod
    async def handler(request: Request, exc: RequestValidationError):
        res = Result()

        error_message = ""
        for error in exc.errors():
            type_of_error = error.get("type", "")
            if type_of_error == TypeOfErrorEnum.json_invalid_error.value:
                error_message = UniversalMessage.request_data_error.value
                break

            if type_of_error == TypeOfErrorEnum.value_error_missing.value:
                try:
                    _, key = error.get("loc", "")
                except:
                    _, data, key = error.get("loc", "")
                error_message = UniversalMessage.key_missing_error.value.format(key)
                break

            if type_of_error == TypeOfErrorEnum.value_error_none.value:
                try:
                    _, key = error.get("loc", "")
                except:
                    _, data, key = error.get("loc", "")
                error_message = UniversalMessage.key_none_error.value.format(key)
                break

            if type_of_error == TypeOfErrorEnum.value_error_max_length.value:
                try:
                    _, key = error.get("loc", "")
                except:
                    _, data, key = error.get("loc", "")
                error_message = key + error.get("msg", "")
                break

            if type_of_error == TypeOfErrorEnum.type_error_list.value:
                try:
                    _, key = error.get("loc", "")
                except:
                    _, data, key = error.get("loc", "")
                error_message = key + error.get("msg", "")
                break

            if type_of_error == TypeOfErrorEnum.value_error_min_length.value:
                try:
                    _, key = error.get("loc", "")
                except:
                    _, data, key = error.get("loc", "")
                error_message = key + " " + error.get("msg", "")
                break
            if type_of_error == TypeOfErrorEnum.type_error.value:
                try:
                    _, key = error.get("loc", "")
                except:
                    _, data, key = error.get("loc", "")
                error_message = UniversalMessage.incorrect_data_error.value.format(key)
                break
            if type_of_error == TypeOfErrorEnum.type_error_none_not_allowed.value:
                try:
                    _, key = error.get("loc", "")
                except:
                    _, data, key = error.get("loc", "")
                error_message = key + " " + error.get("msg", "")
                break
            else:
                error_message = error.get("msg", "")
                break

        start_time = time.time()
        res.result_obj = {"data": {},
                          "error": [],
                          "message": error_message
                          }
        res.result_code = HTTPStatus.bad_request
        end_time = time.time()
        rtn = res.get()
        returnJson = ReturnJson(end_time - start_time, rtn['code'], rtn['object'], rtn['message'])

        return returnJson.get_return_json()
