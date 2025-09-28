import logging

class DisplayConfigQueryHelper:
    """Query helper for display config module - Raw SQL queries"""
    
    @staticmethod
    def _convert_boolean_to_int(value):
        """Convert boolean values to integers for database storage"""
        if isinstance(value, bool):
            return 1 if value else 0
        return value
    
    @staticmethod
    def get_headers_for_grid_query(grid_name_id=None):
        """Get SQL query for grid headers by gridNameId with values formatted"""
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for get_headers_for_grid_query")
        
        query = f"""
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.gridNameId = {grid_name_id} 
            ORDER BY rdc.sortIndex
        """
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - get_headers_for_grid_query: {query}")
        return query
    
    @staticmethod
    def get_all_display_configs_query():
        """Get SQL query for all display configs with grid metadata"""
        query = """
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            ORDER BY gm.gridName, rdc.sortIndex
        """
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - get_all_display_configs_query: {query}")
        return query
    
    @staticmethod
    def get_display_config_by_id_query(config_id=None):
        """Get SQL query for display config by ID with values formatted"""
        if config_id is None:
            raise ValueError("config_id is required for get_display_config_by_id_query")
        
        query = f"""
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.id = {config_id} LIMIT 1
        """
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - get_display_config_by_id_query: {query}")
        return query
    
    @staticmethod
    def get_display_configs_by_grid_query(grid_name_id=None):
        """Get SQL query for display configs by gridNameId with values formatted"""
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for get_display_configs_by_grid_query")
        
        query = f"""
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.gridNameId = {grid_name_id} 
            ORDER BY rdc.sortIndex
        """
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - get_display_configs_by_grid_query: {query}")
        return query
    
    @staticmethod
    def create_display_config_query(grid_name_id=None, display_id=None, title=None, hidden=None, width=None, sort_index=None, ellipsis=None, align=None, db_data_type=None, code_data_type=None, format=None):
        """Get SQL query to create a new display config with values directly bound"""
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for create_display_config_query")
        if display_id is None:
            raise ValueError("display_id is required for create_display_config_query")
        if title is None:
            raise ValueError("title is required for create_display_config_query")
        if sort_index is None:
            raise ValueError("sort_index is required for create_display_config_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['gridNameId', 'displayId', 'title', 'sortIndex']
        values = [str(grid_name_id), f"'{display_id}'", f"'{title}'", str(sort_index)]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if hidden is not None:
            columns.append('hidden')
            values.append(str(DisplayConfigQueryHelper._convert_boolean_to_int(hidden)))
        if width is not None:
            columns.append('width')
            values.append(str(width))
        if ellipsis is not None:
            columns.append('ellipsis')
            values.append(str(DisplayConfigQueryHelper._convert_boolean_to_int(ellipsis)))
        if align is not None:
            columns.append('align')
            values.append(f"'{align}'")
        if db_data_type is not None:
            columns.append('dbDataType')
            values.append(f"'{db_data_type}'")
        if code_data_type is not None:
            columns.append('codeDataType')
            values.append(f"'{code_data_type}'")
        if format is not None:
            columns.append('format')
            values.append(f"'{format}'")
        
        # Create query with values directly bound
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        
        query = f"INSERT INTO result_display_config ({columns_str}) VALUES ({values_str})"
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - create_display_config_query: {query}")
        return query
    
    @staticmethod
    def update_display_config_query(grid_name_id=None, display_id=None, title=None, hidden=None, width=None, sort_index=None, ellipsis=None, align=None, db_data_type=None, code_data_type=None, format=None, config_id=None):
        """Get SQL query to update a display config with values formatted"""
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for update_display_config_query")
        if display_id is None:
            raise ValueError("display_id is required for update_display_config_query")
        if title is None:
            raise ValueError("title is required for update_display_config_query")
        if hidden is None:
            raise ValueError("hidden is required for update_display_config_query")
        if width is None:
            raise ValueError("width is required for update_display_config_query")
        if sort_index is None:
            raise ValueError("sort_index is required for update_display_config_query")
        if ellipsis is None:
            raise ValueError("ellipsis is required for update_display_config_query")
        if align is None:
            raise ValueError("align is required for update_display_config_query")
        if db_data_type is None:
            raise ValueError("db_data_type is required for update_display_config_query")
        if code_data_type is None:
            raise ValueError("code_data_type is required for update_display_config_query")
        if format is None:
            raise ValueError("format is required for update_display_config_query")
        if config_id is None:
            raise ValueError("config_id is required for update_display_config_query")
        
        query = f"""
            UPDATE result_display_config 
            SET gridNameId = {grid_name_id}, displayId = '{display_id}', title = '{title}', hidden = {hidden}, width = {width}, 
                sortIndex = {sort_index}, ellipsis = {ellipsis}, align = '{align}', 
                dbDataType = '{db_data_type}', codeDataType = '{code_data_type}', format = '{format}'
            WHERE id = {config_id}
        """
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - update_display_config_query: {query}")
        return query
    
    @staticmethod
    def delete_display_config_query(config_id=None):
        """Get SQL query to delete a display config with values formatted"""
        if config_id is None:
            raise ValueError("config_id is required for delete_display_config_query")
        
        query = f"DELETE FROM result_display_config WHERE id = {config_id}"
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - delete_display_config_query: {query}")
        return query
    
    @staticmethod
    def get_display_config_by_display_id_query(display_id=None):
        """Get SQL query for display config by displayId with values formatted"""
        if display_id is None:
            raise ValueError("display_id is required for get_display_config_by_display_id_query")
        
        return f"""
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.displayId = '{display_id}' LIMIT 1
        """
    
    # Grid Metadata Queries
    @staticmethod
    def get_grid_metadata_list_query(name=None, is_active=None):
        """Get SQL query for grid metadata list with optional filters"""
        query = "SELECT * FROM grid_metadata WHERE 1=1"
        
        if name:
            query += f" AND gridName LIKE '%{name}%'"
        if is_active is not None:
            query += f" AND is_active = {DisplayConfigQueryHelper._convert_boolean_to_int(is_active)}"
        
        query += " ORDER BY gridName"
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - get_grid_metadata_list_query: {query}")
        return query
    
    @staticmethod
    def get_all_grid_metadata_query():
        """Get SQL query for all grid metadata"""
        return "SELECT * FROM grid_metadata WHERE is_active = 1 ORDER BY gridName"
    
    @staticmethod
    def get_grid_metadata_by_id_query(metadata_id=None):
        """Get SQL query for grid metadata by ID with values formatted"""
        if metadata_id is None:
            raise ValueError("metadata_id is required for get_grid_metadata_by_id_query")
        
        return f"SELECT * FROM grid_metadata WHERE id = {metadata_id} LIMIT 1"
    
    @staticmethod
    def get_grid_metadata_by_grid_name_id_query(grid_name_id=None):
        """Get SQL query for grid metadata by gridNameId with values formatted"""
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for get_grid_metadata_by_grid_name_id_query")
        
        return f"SELECT * FROM grid_metadata WHERE gridNameId = {grid_name_id} LIMIT 1"
    
    @staticmethod
    def create_grid_metadata_query(grid_name=None, grid_name_id=None, description=None, is_active=None):
        """Get SQL query to create a new grid metadata with values directly bound"""
        if grid_name is None:
            raise ValueError("grid_name is required for create_grid_metadata_query")
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for create_grid_metadata_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['gridName', 'gridNameId']
        values = [f"'{grid_name}'", str(grid_name_id)]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if description is not None:
            columns.append('description')
            values.append(f"'{description}'")
        if is_active is not None:
            columns.append('is_active')
            values.append(str(DisplayConfigQueryHelper._convert_boolean_to_int(is_active)))
        
        # Create query with values directly bound
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        
        query = f"INSERT INTO grid_metadata ({columns_str}) VALUES ({values_str})"
        logging.info(f"DISPLAY_CONFIG_QUERY_HELPER: Generated query - create_grid_metadata_query: {query}")
        return query
    
    @staticmethod
    def update_grid_metadata_query(grid_name=None, grid_name_id=None, description=None, is_active=None, metadata_id=None):
        """Get SQL query to update grid metadata with values formatted"""
        if grid_name is None:
            raise ValueError("grid_name is required for update_grid_metadata_query")
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for update_grid_metadata_query")
        if is_active is None:
            raise ValueError("is_active is required for update_grid_metadata_query")
        if metadata_id is None:
            raise ValueError("metadata_id is required for update_grid_metadata_query")
        
        return f"""
            UPDATE grid_metadata 
            SET gridName = '{grid_name}', gridNameId = {grid_name_id}, description = '{description}', is_active = {is_active}
            WHERE id = {metadata_id}
        """
    
    @staticmethod
    def delete_grid_metadata_query(metadata_id=None):
        """Get SQL query to delete grid metadata with values formatted"""
        if metadata_id is None:
            raise ValueError("metadata_id is required for delete_grid_metadata_query")
        
        return f"DELETE FROM grid_metadata WHERE id = {metadata_id}"
    
    @staticmethod
    def update_display_config_by_grid_and_display_id_query(title=None, hidden=None, width=None, sort_index=None, ellipsis=None, align=None, db_data_type=None, code_data_type=None, format=None, grid_name_id=None, display_id=None):
        """Get SQL query to update display config by gridNameId and displayId with values formatted"""
        if title is None:
            raise ValueError("title is required for update_display_config_by_grid_and_display_id_query")
        if hidden is None:
            raise ValueError("hidden is required for update_display_config_by_grid_and_display_id_query")
        if width is None:
            raise ValueError("width is required for update_display_config_by_grid_and_display_id_query")
        if sort_index is None:
            raise ValueError("sort_index is required for update_display_config_by_grid_and_display_id_query")
        if ellipsis is None:
            raise ValueError("ellipsis is required for update_display_config_by_grid_and_display_id_query")
        if align is None:
            raise ValueError("align is required for update_display_config_by_grid_and_display_id_query")
        if db_data_type is None:
            raise ValueError("db_data_type is required for update_display_config_by_grid_and_display_id_query")
        if code_data_type is None:
            raise ValueError("code_data_type is required for update_display_config_by_grid_and_display_id_query")
        if format is None:
            raise ValueError("format is required for update_display_config_by_grid_and_display_id_query")
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for update_display_config_by_grid_and_display_id_query")
        if display_id is None:
            raise ValueError("display_id is required for update_display_config_by_grid_and_display_id_query")
        
        return f"""
            UPDATE result_display_config 
            SET title = '{title}', hidden = {hidden}, width = {width}, sortIndex = {sort_index}, 
                ellipsis = {ellipsis}, align = '{align}', dbDataType = '{db_data_type}', 
                codeDataType = '{code_data_type}', format = '{format}'
            WHERE gridNameId = {grid_name_id} AND displayId = '{display_id}'
        """
    
    @staticmethod
    def delete_display_config_by_grid_and_display_id_query(grid_name_id=None, display_id=None):
        """Get SQL query to delete display config by gridNameId and displayId with values formatted"""
        if grid_name_id is None:
            raise ValueError("grid_name_id is required for delete_display_config_by_grid_and_display_id_query")
        if display_id is None:
            raise ValueError("display_id is required for delete_display_config_by_grid_and_display_id_query")
        
        return f"DELETE FROM result_display_config WHERE gridNameId = {grid_name_id} AND displayId = '{display_id}'"