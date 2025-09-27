import logging
from manager.db_manager import DBManager
from look_up.lookup_models import LookupType, LookupValue
from look_up.query_helper import LookupQueryHelper

class LookUpDao:
    def __init__(self):
        self.db_manager = DBManager.get_instance()

    
    def get_lookup_types(self):
        """Get all lookup types"""
        try:
            query = LookupQueryHelper.get_lookup_types_query()
            rows = self.db_manager.execute_query(query)
            
            lookup_types = []
            for row in rows:
                lookup_type = LookupType.from_dict(row)
                lookup_types.append(lookup_type)
                
            return lookup_types
            
        except Exception as e:
            logging.error(f"Error in get_lookup_types: {e}")
            return []
    
    def get_lookup_values_by_type_name(self, type_name):
        """Get lookup values by type name"""
        try:
            query = LookupQueryHelper.get_lookup_values_by_type_name_query()
            rows = self.db_manager.execute_query(query, (type_name,))
            
            lookup_values = []
            for row in rows:
                lookup_value = LookupValue.from_dict(row)
                lookup_values.append(lookup_value)
                
            return lookup_values
            
        except Exception as e:
            logging.error(f"Error in get_lookup_values_by_type_name: {e}")
            return []
    
    def get_lookup_type_by_name(self, name):
        """Get lookup type by name"""
        try:
            query = LookupQueryHelper.get_lookup_type_by_name_query()
            result = self.db_manager.execute_query(query, (name,))
            
            if result:
                return LookupType.from_dict(result[0])
            return None
            
        except Exception as e:
            logging.error(f"Error in get_lookup_type_by_name: {e}")
            return None
    
    def get_lookup_values_by_type_id(self, type_id):
        """Get lookup values by type ID"""
        try:
            query = LookupQueryHelper.get_lookup_values_by_type_id_query()
            rows = self.db_manager.execute_query(query, (type_id,))
            
            lookup_values = []
            for row in rows:
                lookup_value = LookupValue.from_dict(row)
                lookup_values.append(lookup_value)
                
            return lookup_values
            
        except Exception as e:
            logging.error(f"Error in get_lookup_values_by_type_id: {e}")
            return []
    
    def get_lookup_value_by_id(self, value_id):
        """Get lookup value by ID"""
        try:
            query = LookupQueryHelper.get_lookup_value_by_id_query()
            result = self.db_manager.execute_query(query, (value_id,))
            
            if result:
                return LookupValue.from_dict(result[0])
            return None
            
        except Exception as e:
            logging.error(f"Error in get_lookup_value_by_id: {e}")
            return None
    
    def create_lookup_type(self, name, description=None):
        """Create a new lookup type"""
        try:
            query = LookupQueryHelper.create_lookup_type_query()
            from datetime import datetime
            now = datetime.now()
            type_id = self.db_manager.execute_insert(query, (name, description, now))
            
            return LookupType(id=type_id, name=name, description=description, created_at=now)
            
        except Exception as e:
            logging.error(f"Error in create_lookup_type: {e}")
            raise
    
    def create_lookup_value(self, lookup_type_id, code, value, description=None, is_active=True, sort_order=0):
        """Create a new lookup value"""
        try:
            query = LookupQueryHelper.create_lookup_value_query()
            from datetime import datetime
            now = datetime.now()
            value_id = self.db_manager.execute_insert(query, (
                lookup_type_id, code, value, description, is_active, sort_order, now
            ))
            
            return LookupValue(
                id=value_id, lookup_type_id=lookup_type_id, code=code, 
                value=value, description=description, is_active=is_active, 
                sort_order=sort_order, created_at=now
            )
            
        except Exception as e:
            logging.error(f"Error in create_lookup_value: {e}")
            raise
    
    def update_lookup_type(self, type_id, name=None, description=None):
        """Update lookup type"""
        try:
            query = LookupQueryHelper.update_lookup_type_query()
            self.db_manager.execute_update(query, (name, description, type_id))
            return True
            
        except Exception as e:
            logging.error(f"Error in update_lookup_type: {e}")
            return False
    
    def update_lookup_value(self, value_id, code=None, value=None, description=None, is_active=None, sort_order=None):
        """Update lookup value"""
        try:
            query = LookupQueryHelper.update_lookup_value_query()
            self.db_manager.execute_update(query, (code, value, description, is_active, sort_order, value_id))
            return True
            
        except Exception as e:
            logging.error(f"Error in update_lookup_value: {e}")
            return False
    
    def delete_lookup_type(self, type_id):
        """Delete lookup type"""
        try:
            query = LookupQueryHelper.delete_lookup_type_query()
            self.db_manager.execute_update(query, (type_id,))
            return True
            
        except Exception as e:
            logging.error(f"Error in delete_lookup_type: {e}")
            return False
    
    def delete_lookup_value(self, value_id):
        """Delete lookup value"""
        try:
            query = LookupQueryHelper.delete_lookup_value_query()
            self.db_manager.execute_update(query, (value_id,))
            return True
            
        except Exception as e:
            logging.error(f"Error in delete_lookup_value: {e}")
            return False
    
    def look_up(self, type_name):
        """Get lookup values by type name - main method for backward compatibility"""
        return self.get_lookup_values_by_type_name(type_name)