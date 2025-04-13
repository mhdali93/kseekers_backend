import logging
from look_up.query_helper import QueryHelpers
from manager.db_manager import DBManager, DBSessionManager
from models.ormmodel import ResultDisplayConfig

class LookUpDao:
    def __init__(self):
        self.q_helper = QueryHelpers()
        self.db_manager = DBManager.get_instance()

    def look_up(self, header_type):
        """Get headers using SQLModel session"""
        try:
            # First method using SQLModel ORM
            stmt = self.q_helper.get_headers_for_grid(header_type)
            with DBSessionManager() as session:
                headers = session.exec(stmt).all()
                
            if headers:
                logging.info(f"Found {len(headers)} headers with SQLModel")
                return headers
                
            # If no results from SQLModel, try direct SQL
            return self.look_up_direct_sql(header_type)
        except Exception as e:
            logging.error(f"Error in look_up: {e}")
            # Fallback to direct SQL if SQLModel fails
            return self.look_up_direct_sql(header_type)
            
    def look_up_direct_sql(self, header_type):
        """Get headers using direct SQL query with connection pool"""
        logging.info(f"Getting headers with direct SQL for type: {header_type}")
        try:
            query = """
            SELECT * FROM result_display_config 
            WHERE type = ? 
            ORDER BY sortIndex
            """
            
            rows = self.db_manager.execute_query(query, (header_type,))
            
            # Convert the results to a list of ResultDisplayConfig objects
            headers = []
            for row in rows:
                config = ResultDisplayConfig(
                    id=row['id'],
                    displayId=row['displayId'],
                    title=row['title'],
                    key=row['key'],
                    hidden=row['hidden'],
                    sorter=row['sorter'],
                    width=row['width'],
                    fixed=row['fixed'],
                    dataIndex=row['dataIndex'],
                    sortIndex=row['sortIndex'],
                    type=row['type'],
                    ellipsis=row['ellipsis'],
                    align=row['align'],
                    dataType=row['dataType'],
                    format=row['format']
                )
                headers.append(config)
                
            logging.info(f"Found {len(headers)} headers with direct SQL")
            return headers
            
        except Exception as e:
            logging.error(f"Error in look_up_direct_sql: {e}")
            return []
