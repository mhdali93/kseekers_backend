import traceback
import logging
from fastapi.encoders import jsonable_encoder
from look_up.dao import LookUpDao


class LookUpController:
    def __init__(self):
        self.dao = LookUpDao()

    def get_lookup_types(self):
        """Get all lookup types"""
        try:
            return self.dao.get_lookup_types()
        except Exception as e:
            logging.error(f"Error in get_lookup_types: {e}")
            raise e
    
    def get_lookup_values_by_type(self, type_name):
        """Get lookup values by type name"""
        try:
            if not type_name or len(type_name.strip()) < 1:
                raise ValueError("Type name is required")
            return self.dao.get_lookup_values_by_type_name(type_name)
        except Exception as e:
            logging.error(f"Error in get_lookup_values_by_type: {e}")
            raise e
    
    def manage_lookup_type(self, type_data):
        """Create or update lookup type (upsert by name)"""
        try:
            if not type_data.get('name') or len(type_data['name'].strip()) < 1:
                raise ValueError("Type name is required")
            
            # Check if type exists
            existing_type = self.dao.get_lookup_type_by_name(type_data['name'])
            
            if existing_type:
                # Update existing type
                return self.dao.update_lookup_type(
                    existing_type.id, 
                    type_data['name'], 
                    type_data.get('description')
                )
            else:
                # Create new type
                return self.dao.create_lookup_type(
                    type_data['name'], 
                    type_data.get('description')
                )
        except Exception as e:
            logging.error(f"Error in manage_lookup_type: {e}")
            raise e
    
    def manage_lookup_values(self, type_name, values):
        """Create or update lookup values for a type (upsert by code)"""
        try:
            if not type_name or len(type_name.strip()) < 1:
                raise ValueError("Type name is required")
            
            if not values:
                raise ValueError("Values list cannot be empty")
            
            # Get or create the lookup type
            lookup_type = self.dao.get_lookup_type_by_name(type_name)
            if not lookup_type:
                raise ValueError(f"Lookup type '{type_name}' not found")
            
            # Get existing values for this type
            existing_values = self.dao.get_lookup_values_by_type_name(type_name)
            existing_codes = {value.code for value in existing_values}
            
            # Process each value in the request
            new_codes = set()
            for value in values:
                code = value['code']
                new_codes.add(code)
                
                if code in existing_codes:
                    # Update existing value
                    self.dao.update_lookup_value_by_type_and_code(
                        lookup_type.id, code, value
                    )
                else:
                    # Create new value
                    self.dao.create_lookup_value(
                        lookup_type.id,
                        value['code'],
                        value['value'],
                        value.get('description'),
                        value.get('is_active', True),
                        value.get('sort_order', 0)
                    )
            
            # Remove values that are no longer in the request
            codes_to_remove = existing_codes - new_codes
            for code in codes_to_remove:
                self.dao.delete_lookup_value_by_type_and_code(lookup_type.id, code)
            
            return True
        except Exception as e:
            logging.error(f"Error in manage_lookup_values: {e}")
            raise e