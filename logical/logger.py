from functools import wraps
from fastapi import Request
from models.result import Result
from models.enums import AppStatus
import uuid
import logging
import config


def log_request(func):
    @wraps(func)
    async def wrapper( *args, **kwargs):

        request = kwargs.get('request')
        res = Result()
        request_id = str(uuid.uuid4())

        message = {
            'host': str(request.base_url.hostname),
            'args': str(kwargs),
            'client': str(request.client.host),
            'port': str(request.client.port),
            'path_params': str(request.path_params),
            'query_params': str(request.query_params),
            'scope': str(request.scope),
            'is_secure': str(request.url.is_secure),
            'resource_path': str(request.url.path),
            'username': str(request.url.username),
            'query': str(request.url.query),
            'header': str(request.headers)
        }

        try:
            logging.info(f"Request: {request_id} - {message}")
            res.set(AppStatus.success, request_id, 0)

        except Exception as e:
            logging.error(f"Logging error: {e}")
            res.set(AppStatus.logging_error, e)

        finally:
            kwargs['logger'] = res

        return await func(*args, **kwargs)

    return wrapper


def log_response(resp, request_id, row_count=0):
    res = Result()
    try:
        logging.info(f"Response: {request_id} - {resp}")
        res.set(AppStatus.success, request_id, row_count)

    except Exception as e:
        logging.error(f"Logging error: {e}")
        res.set(AppStatus.logging_error, e, row_count=0)

    finally:
        return res


def update_log(logger, rj):
    if logger.result_code == AppStatus.success:
        rj.set_request_logging_status(AppStatus.success.value)
        resp_log = log_response(rj.serialize(), logger.result_obj)
        if resp_log.result_code == AppStatus.success:
            rj.set_response_logging_status(AppStatus.success.value)
        else:
            rj.set_response_logging_status(AppStatus.logging_error.value)
    else:
        rj.set_request_logging_status(AppStatus.logging_error.value)
