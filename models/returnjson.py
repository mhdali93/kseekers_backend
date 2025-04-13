from fastapi.responses import JSONResponse


class ReturnJson:
    def __init__(self, fetch_time=None, status_and_code=None, rjson={}, row_count=0, message=""):
        self.http_status = None
        self.fetch_time = None
        self.result_json = None
        self.request_logging_status = None
        self.response_logging_status = None
        self.result_json = rjson
        self.fetch_time = fetch_time
        self.row_count = row_count
        self.status = status_and_code.value[1] if status_and_code else None
        self.http_status = status_and_code.value[0] if status_and_code else None
        self.message = None

    def set_http_status(self, status):
        self.http_status = status.value[0]
        self.status = status.value[1]

    def set_message(self, message=" "):
        self.message = message

    def set_result_json(self, rjson):
        self.result_json = rjson

    def set_fetch_time(self, ftime):
        self.fetch_time = ftime

    def set_request_logging_status(self, req_status):
        self.request_logging_status = req_status

    def set_response_logging_status(self, resp_status):
        self.response_logging_status = resp_status

    def get_return_json(self):
        value = JSONResponse(status_code=self.http_status,
                             content={
                                 'status': self.status,
                                 'fetch_time': self.fetch_time,
                                 'row_count': self.row_count,
                                 'result': {'payload': self.result_json["data"],
                                            'errorStack': self.result_json["error"],
                                            'message': self.result_json["message"]},
                                 'request_logging': self.request_logging_status,
                                 'response_logging': self.response_logging_status

                             })
        return value

    def serialize(self):
        return {'status_code': self.http_status,
                'content': {
                    'status': self.status,
                    'fetch_time': self.fetch_time,
                    'row_count': self.row_count,
                    'result': {'payload': self.result_json["data"], 'errorStack': self.result_json["error"],
                               'message': self.result_json["message"]},
                    'request_logging': self.request_logging_status,
                    'response_logging': self.response_logging_status
                }
                }
