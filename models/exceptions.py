from typing import Any, Union

from fastapi import HTTPException

from models.enums import ExceptionMessage, HTTPStatus


class AWSConnectionException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_connecion_error.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class AWSS3WriteException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_s3_write_exception.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class AWSS3PresignedURLException(Exception):
    def __init__(self, obj, message=ExceptionMessage.aws_s3_download_exception.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class DBConnectionException(Exception):
    def __init__(self, obj, message=ExceptionMessage.db_connection_error.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class DBCursorFetchException(Exception):
    def __init__(self, obj, message=ExceptionMessage.db_cursor_fetch_error.value):
        self.object = obj
        self.message = message
        super().__init__(self.message)


class CustomException(HTTPException):
    def __init__(self, status_code: int, status: HTTPStatus, fetch_time: Union[int, float], row_count: int, result: Any,
                 request_logging: Any, response_logging: Any):
        self.status_code = status_code
        self.status = status
        self.fetch_time = fetch_time
        self.row_count = row_count
        self.result = result
        self.request_logging = request_logging
        self.response_logging = response_logging
        super().__init__(status_code=self.status_code, detail=None)
