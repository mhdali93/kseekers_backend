import logging
from display_config.dao import DisplayConfigDAO

class DisplayConfigController:
    """Controller for display config business logic"""
    
    def __init__(self):
        self.dao = DisplayConfigDAO()
    
    # Grid Metadata Methods
    def create_grid_metadata(self, grid_data):
        """Create a new grid metadata with validation"""
        try:
            if not grid_data.get('gridName') or len(grid_data['gridName'].strip()) < 1:
                raise ValueError("Grid Name is required")
            
            if not grid_data.get('gridNameId') or len(grid_data['gridNameId'].strip()) < 1:
                raise ValueError("Grid Name ID is required")
            
            grid_metadata = self.dao.create_grid_metadata(
                grid_data.get('gridName'),
                grid_data.get('gridNameId'),
                grid_data.get('description')
            )
            logging.info(f"DISPLAY_CONFIG_CONTROLLER: Grid metadata created - grid_name={grid_data.get('gridName')}")
            return grid_metadata.id
        except Exception as e:
            logging.error(f"DISPLAY_CONFIG_CONTROLLER: Error creating grid metadata - grid_name={grid_data.get('gridName', 'unknown')}, error={str(e)}")
            raise
    
    def list_grid_metadata(self, name=None, is_active=None):
        """List grid metadata with optional filters"""
        grid_metadata_list = self.dao.get_grid_metadata_list(name, is_active)
        return [grid.to_dict() for grid in grid_metadata_list]
    
    def update_grid_metadata(self, grid_id, grid_data):
        """Update grid metadata with validation"""
        try:
            # Validate grid exists
            existing = self.dao.get_grid_metadata_by_id(grid_id)
            if not existing:
                logging.error(f"DISPLAY_CONFIG_CONTROLLER: Grid metadata not found - grid_id={grid_id}")
                raise ValueError("Grid metadata not found")
            
            # Validate required fields if provided
            if 'gridName' in grid_data and (not grid_data['gridName'] or len(grid_data['gridName'].strip()) < 1):
                raise ValueError("Grid Name cannot be empty")
            
            result = self.dao.update_grid_metadata(grid_id, **grid_data)
            logging.info(f"DISPLAY_CONFIG_CONTROLLER: Grid metadata updated - grid_id={grid_id}")
            return result
        except Exception as e:
            logging.error(f"DISPLAY_CONFIG_CONTROLLER: Error updating grid metadata - grid_id={grid_id}, error={str(e)}")
            raise
    
    # Result Display Config Methods
    def list_display_configs(self, grid_name_id):
        """List display configs by gridNameId"""
        if not grid_name_id or len(grid_name_id.strip()) < 1:
            raise ValueError("Grid Name ID is required")
        
        display_configs = self.dao.get_display_configs_by_grid(grid_name_id)
        return [config.to_dict() for config in display_configs]
    
    def update_display_configs(self, grid_name_id, configs):
        """Update display configs with upsert logic"""
        try:
            if not grid_name_id or len(grid_name_id.strip()) < 1:
                raise ValueError("Grid Name ID is required")
            
            if not configs:
                raise ValueError("Configs list cannot be empty")
            
            # Validate each config item
            for config in configs:
                if not config.get('displayId') or len(config['displayId'].strip()) < 1:
                    raise ValueError("Display ID is required for all configs")
                
                if not config.get('title') or len(config['title'].strip()) < 1:
                    raise ValueError("Title is required for all configs")
            
            result = self.dao.upsert_display_configs(grid_name_id, configs)
            logging.info(f"DISPLAY_CONFIG_CONTROLLER: Display configs updated - grid_name_id={grid_name_id}, count={len(configs)}")
            return result
        except Exception as e:
            logging.error(f"DISPLAY_CONFIG_CONTROLLER: Error updating display configs - grid_name_id={grid_name_id}, error={str(e)}")
            raise
