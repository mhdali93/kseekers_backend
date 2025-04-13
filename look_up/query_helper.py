import logging
from sqlmodel import select
from models.ormmodel import ResultDisplayConfig


class QueryHelpers:
    @staticmethod
    def get_headers_for_grid(header_type: str):
        query = select(ResultDisplayConfig).where(
            ResultDisplayConfig.type == header_type).order_by(ResultDisplayConfig.sortIndex)
        
        logging.info(query.compile(compile_kwargs={"literal_binds": True}))
        return query
