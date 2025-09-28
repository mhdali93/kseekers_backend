from display_config.dao import DisplayConfigDAO

class DisplayConfigController:
    """Controller for display config business logic"""
    
    def __init__(self):
        self.dao = DisplayConfigDAO()
    
    # Grid Metadata Methods
    def create_grid_metadata(self, grid_data):
        """Create a new grid metadata with validation"""
        if not grid_data.get('gridName') or len(grid_data['gridName'].strip()) < 1:
            raise ValueError("Grid Name is required")
        
        if not grid_data.get('gridNameId') or len(grid_data['gridNameId'].strip()) < 1:
            raise ValueError("Grid Name ID is required")
        
        return self.dao.create_grid_metadata(
            grid_data.get('gridName'),
            grid_data.get('gridNameId'),
            grid_data.get('description'),
            grid_data.get('is_active', 1)
        )
    
    def list_grid_metadata(self, name=None, is_active=None):
        """List grid metadata with optional filters"""
        return self.dao.get_grid_metadata_list(name, is_active)
    
    def update_grid_metadata(self, grid_id, grid_data):
        """Update grid metadata with validation"""
        # Validate grid exists
        existing = self.dao.get_grid_metadata_by_id(grid_id)
        if not existing:
            raise ValueError("Grid metadata not found")
        
        # Validate required fields if provided
        if 'gridName' in grid_data and (not grid_data['gridName'] or len(grid_data['gridName'].strip()) < 1):
            raise ValueError("Grid Name cannot be empty")
        
        return self.dao.update_grid_metadata(grid_id, grid_data)
    
    # Result Display Config Methods
    def list_display_configs(self, grid_name_id):
        """List display configs by gridNameId"""
        if not grid_name_id or len(grid_name_id.strip()) < 1:
            raise ValueError("Grid Name ID is required")
        
        return self.dao.get_display_configs_by_grid(grid_name_id)
    
    def update_display_configs(self, grid_name_id, configs):
        """Update display configs with upsert logic"""
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
        
        return self.dao.upsert_display_configs(grid_name_id, configs)
