from display_config.dao import DisplayConfigDAO

class DisplayConfigController:
    """Controller for display config business logic"""
    
    def __init__(self):
        self.dao = DisplayConfigDAO()
    
    def get_headers_for_grid(self, grid_name_id):
        """Get headers for grid by gridNameId"""
        return self.dao.get_headers_for_grid(grid_name_id)
    
    def get_all_display_configs(self):
        """Get all display configs"""
        return self.dao.get_all_display_configs()
    
    def get_display_config(self, config_id):
        """Get display config by ID"""
        return self.dao.get_display_config_by_id(config_id)
    
    def get_display_configs_by_grid(self, grid_name_id):
        """Get display configs by gridNameId"""
        return self.dao.get_display_configs_by_grid(grid_name_id)
    
    def create_display_config(self, config_data):
        """Create a new display config with validation"""
        # Business logic validation
        if not config_data.get('displayId') or len(config_data['displayId'].strip()) < 1:
            raise ValueError("Display ID is required")
        
        if not config_data.get('title') or len(config_data['title'].strip()) < 1:
            raise ValueError("Title is required")
        
        if not config_data.get('gridNameId') or len(config_data['gridNameId'].strip()) < 1:
            raise ValueError("Grid Name ID is required")
        
        return self.dao.create_display_config(
            config_data.get('gridNameId'),
            config_data.get('displayId'),
            config_data.get('title'),
            config_data.get('hidden', 0),
            config_data.get('width'),
            config_data.get('sortIndex', 0),
            config_data.get('ellipsis'),
            config_data.get('align'),
            config_data.get('dbDataType'),
            config_data.get('codeDataType'),
            config_data.get('format')
        )
    
    def update_display_config(self, config_id, config_data):
        """Update display config with validation"""
        # Validate config exists
        existing = self.dao.get_display_config_by_id(config_id)
        if not existing:
            raise ValueError("Display config not found")
        
        # Validate required fields if provided
        if 'displayId' in config_data and (not config_data['displayId'] or len(config_data['displayId'].strip()) < 1):
            raise ValueError("Display ID cannot be empty")
        
        if 'title' in config_data and (not config_data['title'] or len(config_data['title'].strip()) < 1):
            raise ValueError("Title cannot be empty")
        
        if 'gridNameId' in config_data and (not config_data['gridNameId'] or len(config_data['gridNameId'].strip()) < 1):
            raise ValueError("Grid Name ID cannot be empty")
        
        return self.dao.update_display_config(config_id, config_data)
    
    def delete_display_config(self, config_id):
        """Delete display config"""
        # Validate config exists
        existing = self.dao.get_display_config_by_id(config_id)
        if not existing:
            raise ValueError("Display config not found")
        
        return self.dao.delete_display_config(config_id)
    
    def get_all_grid_metadata(self):
        """Get all grid metadata"""
        return self.dao.get_all_grid_metadata()
