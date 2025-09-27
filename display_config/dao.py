import logging
from manager.db_manager import DBManager
from display_config.display_config_models import ResultDisplayConfig, GridMetadata
from display_config.query_helper import DisplayConfigQueryHelper

class DisplayConfigDAO:
    """Data Access Object for Display Config operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    def get_headers_for_grid(self, grid_name_id):
        """Get display config headers for a specific grid by gridNameId"""
        try:
            query = DisplayConfigQueryHelper.get_headers_for_grid_query()
            results = self.db_manager.execute_query(query, (grid_name_id,))
            
            return [ResultDisplayConfig.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting headers for grid {grid_name_id}: {e}")
            raise
    
    def get_all_display_configs(self):
        """Get all display configurations"""
        try:
            query = DisplayConfigQueryHelper.get_all_display_configs_query()
            results = self.db_manager.execute_query(query)
            
            return [ResultDisplayConfig.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting all display configs: {e}")
            raise
    
    def get_display_config_by_id(self, config_id):
        """Get display config by ID"""
        try:
            query = DisplayConfigQueryHelper.get_display_config_by_id_query()
            result = self.db_manager.execute_query(query, (config_id,))
            
            if result:
                return ResultDisplayConfig.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting display config by ID {config_id}: {e}")
            raise
    
    def get_display_configs_by_grid(self, grid_name_id):
        """Get display configs by gridNameId"""
        try:
            query = DisplayConfigQueryHelper.get_display_configs_by_grid_query()
            results = self.db_manager.execute_query(query, (grid_name_id,))
            
            return [ResultDisplayConfig.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting display configs by grid {grid_name_id}: {e}")
            raise
    
    def create_display_config(self, grid_name_id, display_id, title, hidden=0, width=None, sortIndex=0, 
                            ellipsis=None, align=None, db_data_type=None, code_data_type=None, format=None):
        """Create a new display config"""
        try:
            query = DisplayConfigQueryHelper.create_display_config_query()
            config_id = self.db_manager.execute_insert(query, (
                grid_name_id, display_id, title, hidden, width, sortIndex, 
                ellipsis, align, db_data_type, code_data_type, format
            ))
            
            return ResultDisplayConfig(
                id=config_id, gridNameId=grid_name_id, displayId=display_id, title=title, 
                hidden=hidden, width=width, sortIndex=sortIndex, ellipsis=ellipsis,
                align=align, dbDataType=db_data_type, codeDataType=code_data_type, format=format
            )
        except Exception as e:
            logging.error(f"Error creating display config: {e}")
            raise
    
    def update_display_config(self, config_id, **kwargs):
        """Update display config fields"""
        try:
            if not kwargs:
                return False
            
            # Get current config
            current_config = self.get_display_config_by_id(config_id)
            if not current_config:
                return False
            
            # Update fields
            for field, value in kwargs.items():
                if hasattr(current_config, field):
                    setattr(current_config, field, value)
            
            query = DisplayConfigQueryHelper.update_display_config_query()
            rows_affected = self.db_manager.execute_update(query, (
                current_config.gridNameId, current_config.displayId, current_config.title, 
                current_config.hidden, current_config.width, current_config.sortIndex,
                current_config.ellipsis, current_config.align, current_config.dbDataType,
                current_config.codeDataType, current_config.format, config_id
            ))
            
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error updating display config {config_id}: {e}")
            raise
    
    def delete_display_config(self, config_id):
        """Delete display config"""
        try:
            query = DisplayConfigQueryHelper.delete_display_config_query()
            rows_affected = self.db_manager.execute_update(query, (config_id,))
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error deleting display config {config_id}: {e}")
            raise
    
    def get_display_config_by_display_id(self, display_id):
        """Get display config by displayId"""
        try:
            query = DisplayConfigQueryHelper.get_display_config_by_display_id_query()
            result = self.db_manager.execute_query(query, (display_id,))
            
            if result:
                return ResultDisplayConfig.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting display config by displayId {display_id}: {e}")
            raise
    
    # Grid Metadata Methods
    def get_all_grid_metadata(self):
        """Get all grid metadata"""
        try:
            query = DisplayConfigQueryHelper.get_all_grid_metadata_query()
            results = self.db_manager.execute_query(query)
            
            return [GridMetadata.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting all grid metadata: {e}")
            raise
    
    def get_grid_metadata_by_id(self, grid_id):
        """Get grid metadata by ID"""
        try:
            query = DisplayConfigQueryHelper.get_grid_metadata_by_id_query()
            result = self.db_manager.execute_query(query, (grid_id,))
            
            if result:
                return GridMetadata.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting grid metadata by ID {grid_id}: {e}")
            raise
    
    def get_grid_metadata_by_grid_name_id(self, grid_name_id):
        """Get grid metadata by gridNameId"""
        try:
            query = DisplayConfigQueryHelper.get_grid_metadata_by_grid_name_id_query()
            result = self.db_manager.execute_query(query, (grid_name_id,))
            
            if result:
                return GridMetadata.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting grid metadata by gridNameId {grid_name_id}: {e}")
            raise
    
    def create_grid_metadata(self, grid_name, grid_name_id, description=None, is_active=1):
        """Create a new grid metadata"""
        try:
            query = DisplayConfigQueryHelper.create_grid_metadata_query()
            grid_id = self.db_manager.execute_insert(query, (
                grid_name, grid_name_id, description, is_active
            ))
            
            return GridMetadata(
                id=grid_id, gridName=grid_name, gridNameId=grid_name_id, 
                description=description, is_active=is_active
            )
        except Exception as e:
            logging.error(f"Error creating grid metadata: {e}")
            raise
    
    def update_grid_metadata(self, grid_id, **kwargs):
        """Update grid metadata fields"""
        try:
            if not kwargs:
                return False
            
            # Get current grid metadata
            current_grid = self.get_grid_metadata_by_id(grid_id)
            if not current_grid:
                return False
            
            # Update fields
            for field, value in kwargs.items():
                if hasattr(current_grid, field):
                    setattr(current_grid, field, value)
            
            query = DisplayConfigQueryHelper.update_grid_metadata_query()
            rows_affected = self.db_manager.execute_update(query, (
                current_grid.gridName, current_grid.gridNameId, current_grid.description,
                current_grid.is_active, grid_id
            ))
            
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error updating grid metadata {grid_id}: {e}")
            raise
    
    def delete_grid_metadata(self, grid_id):
        """Delete grid metadata"""
        try:
            query = DisplayConfigQueryHelper.delete_grid_metadata_query()
            rows_affected = self.db_manager.execute_update(query, (grid_id,))
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error deleting grid metadata {grid_id}: {e}")
            raise