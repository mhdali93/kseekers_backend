import traceback
import logging
from fastapi.encoders import jsonable_encoder
from look_up.dao import LookUpDao


class LookUpController:
    def __init__(self):
        self.dao = LookUpDao()

    def get_headers_info(self, header_type):
        try:
            headers = self.dao.look_up(header_type)
            logging.info(f"Lookup Headers: {headers}")
            if headers:
                headers = jsonable_encoder(headers)
                logging.info(f'Got Headers length {len(headers)}')
                response = headers

            else:
                response = None

            return response

        except Exception as e:
            logging.error("Inside Exception Block get_headers_info")
            traceback.print_tb(e.__traceback__)
            raise e
