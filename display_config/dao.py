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
    
    def upsert_display_configs(self, grid_name_id, configs):
        """Upsert display configs - update existing or insert new, remove extras"""
        try:
            # Get existing configs for this grid
            existing_configs = self.get_display_configs_by_grid(grid_name_id)
            existing_display_ids = {config.displayId for config in existing_configs}
            
            # Process each config in the request
            new_display_ids = set()
            for config in configs:
                display_id = config['displayId']
                new_display_ids.add(display_id)
                
                if display_id in existing_display_ids:
                    # Update existing config
                    self.update_display_config_by_grid_and_display_id(
                        grid_name_id, display_id, config
                    )
                else:
                    # Insert new config
                    self.create_display_config(
                        grid_name_id,
                        config['displayId'],
                        config['title'],
                        config.get('hidden', 0),
                        config.get('width'),
                        config.get('sortIndex', 0),
                        config.get('ellipsis'),
                        config.get('align'),
                        config.get('dbDataType'),
                        config.get('codeDataType'),
                        config.get('format')
                    )
            
            # Remove configs that are no longer in the request
            configs_to_remove = existing_display_ids - new_display_ids
            for display_id in configs_to_remove:
                self.delete_display_config_by_grid_and_display_id(grid_name_id, display_id)
            
            return True
        except Exception as e:
            logging.error(f"Error upserting display configs for grid {grid_name_id}: {e}")
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
    def get_grid_metadata_list(self, name=None, is_active=None):
        """Get grid metadata list with optional filters"""
        try:
            query = DisplayConfigQueryHelper.get_grid_metadata_list_query(name, is_active)
            params = []
            if name:
                params.append(f"%{name}%")
            if is_active is not None:
                params.append(is_active)
            
            results = self.db_manager.execute_query(query, tuple(params))
            return [GridMetadata.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting grid metadata list: {e}")
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
    
    def update_display_config_by_grid_and_display_id(self, grid_name_id, display_id, config_data):
        """Update display config by gridNameId and displayId"""
        try:
            query = DisplayConfigQueryHelper.update_display_config_by_grid_and_display_id_query()
            rows_affected = self.db_manager.execute_update(query, (
                config_data['title'],
                config_data.get('hidden', 0),
                config_data.get('width'),
                config_data.get('sortIndex', 0),
                config_data.get('ellipsis'),
                config_data.get('align'),
                config_data.get('dbDataType'),
                config_data.get('codeDataType'),
                config_data.get('format'),
                grid_name_id,
                display_id
            ))
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error updating display config by grid and display ID: {e}")
            raise
    
    def delete_display_config_by_grid_and_display_id(self, grid_name_id, display_id):
        """Delete display config by gridNameId and displayId"""
        try:
            query = DisplayConfigQueryHelper.delete_display_config_by_grid_and_display_id_query()
            rows_affected = self.db_manager.execute_update(query, (grid_name_id, display_id))
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error deleting display config by grid and display ID: {e}")
            raise