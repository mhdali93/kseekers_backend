class DisplayConfigQueryHelper:
    """Query helper for display config module - Raw SQL queries"""
    
    @staticmethod
    def get_headers_for_grid_query():
        """Get SQL query for grid headers by gridNameId"""
        return """
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.gridNameId = %s 
            ORDER BY rdc.sortIndex
        """
    
    @staticmethod
    def get_all_display_configs_query():
        """Get SQL query for all display configs with grid metadata"""
        return """
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            ORDER BY gm.gridName, rdc.sortIndex
        """
    
    @staticmethod
    def get_display_config_by_id_query():
        """Get SQL query for display config by ID"""
        return """
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.id = %s LIMIT 1
        """
    
    @staticmethod
    def get_display_configs_by_grid_query():
        """Get SQL query for display configs by gridNameId"""
        return """
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.gridNameId = %s 
            ORDER BY rdc.sortIndex
        """
    
    @staticmethod
    def create_display_config_query():
        """Get SQL query to create a new display config"""
        return """
            INSERT INTO result_display_config (gridNameId, displayId, title, hidden, width, sortIndex, ellipsis, align, dbDataType, codeDataType, format)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def update_display_config_query():
        """Get SQL query to update a display config"""
        return """
            UPDATE result_display_config 
            SET gridNameId = %s, displayId = %s, title = %s, hidden = %s, width = %s, 
                sortIndex = %s, ellipsis = %s, align = %s, 
                dbDataType = %s, codeDataType = %s, format = %s
            WHERE id = %s
        """
    
    @staticmethod
    def delete_display_config_query():
        """Get SQL query to delete a display config"""
        return "DELETE FROM result_display_config WHERE id = %s"
    
    @staticmethod
    def get_display_config_by_display_id_query():
        """Get SQL query for display config by displayId"""
        return """
            SELECT rdc.*, gm.gridName 
            FROM result_display_config rdc
            JOIN grid_metadata gm ON rdc.gridNameId = gm.gridNameId
            WHERE rdc.displayId = %s LIMIT 1
        """
    
    # Grid Metadata Queries
    @staticmethod
    def get_grid_metadata_list_query(name=None, is_active=None):
        """Get SQL query for grid metadata list with optional filters"""
        query = "SELECT * FROM grid_metadata WHERE 1=1"
        params = []
        
        if name:
            query += " AND gridName LIKE %s"
        if is_active is not None:
            query += " AND is_active = %s"
        
        query += " ORDER BY gridName"
        return query
    
    @staticmethod
    def get_all_grid_metadata_query():
        """Get SQL query for all grid metadata"""
        return "SELECT * FROM grid_metadata WHERE is_active = 1 ORDER BY gridName"
    
    @staticmethod
    def get_grid_metadata_by_id_query():
        """Get SQL query for grid metadata by ID"""
        return "SELECT * FROM grid_metadata WHERE id = %s LIMIT 1"
    
    @staticmethod
    def get_grid_metadata_by_grid_name_id_query():
        """Get SQL query for grid metadata by gridNameId"""
        return "SELECT * FROM grid_metadata WHERE gridNameId = %s LIMIT 1"
    
    @staticmethod
    def create_grid_metadata_query():
        """Get SQL query to create a new grid metadata"""
        return """
            INSERT INTO grid_metadata (gridName, gridNameId, description, is_active)
            VALUES (%s, %s, %s, %s)
        """
    
    @staticmethod
    def update_grid_metadata_query():
        """Get SQL query to update grid metadata"""
        return """
            UPDATE grid_metadata 
            SET gridName = %s, gridNameId = %s, description = %s, is_active = %s
            WHERE id = %s
        """
    
    @staticmethod
    def delete_grid_metadata_query():
        """Get SQL query to delete grid metadata"""
        return "DELETE FROM grid_metadata WHERE id = %s"
    
    @staticmethod
    def update_display_config_by_grid_and_display_id_query():
        """Get SQL query to update display config by gridNameId and displayId"""
        return """
            UPDATE result_display_config 
            SET title = %s, hidden = %s, width = %s, sortIndex = %s, 
                ellipsis = %s, align = %s, dbDataType = %s, 
                codeDataType = %s, format = %s
            WHERE gridNameId = %s AND displayId = %s
        """
    
    @staticmethod
    def delete_display_config_by_grid_and_display_id_query():
        """Get SQL query to delete display config by gridNameId and displayId"""
        return "DELETE FROM result_display_config WHERE gridNameId = %s AND displayId = %s"