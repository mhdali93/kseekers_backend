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
            logging.error(f"LOOKUP_DAO: Error getting lookup types - error={str(e)}")
            return []
    
    def get_lookup_values_by_type_name(self, type_name):
        """Get lookup values by type name"""
        try:
            query = LookupQueryHelper.get_lookup_values_by_type_name_query(type_name=type_name)
            rows = self.db_manager.execute_query(query)
            
            lookup_values = []
            for row in rows:
                lookup_value = LookupValue.from_dict(row)
                lookup_values.append(lookup_value)
                
            return lookup_values
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error getting lookup values by type - type_name={type_name}, error={str(e)}")
            return []
    
    def get_lookup_type_by_name(self, name):
        """Get lookup type by name"""
        try:
            query = LookupQueryHelper.get_lookup_type_by_name_query(name=name)
            result = self.db_manager.execute_query(query)
            
            if result:
                return LookupType.from_dict(result[0])
            return None
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error getting lookup type by name - name={name}, error={str(e)}")
            return None
    
    def get_lookup_values_by_type_id(self, type_id):
        """Get lookup values by type ID"""
        try:
            query = LookupQueryHelper.get_lookup_values_by_type_id_query(lookup_type_id=type_id)
            rows = self.db_manager.execute_query(query)
            
            lookup_values = []
            for row in rows:
                lookup_value = LookupValue.from_dict(row)
                lookup_values.append(lookup_value)
                
            return lookup_values
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error getting lookup values by type ID - type_id={type_id}, error={str(e)}")
            return []
    
    def get_lookup_value_by_id(self, value_id):
        """Get lookup value by ID"""
        try:
            query = LookupQueryHelper.get_lookup_value_by_id_query(value_id=value_id)
            result = self.db_manager.execute_query(query)
            
            if result:
                return LookupValue.from_dict(result[0])
            return None
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error getting lookup value by ID - value_id={value_id}, error={str(e)}")
            return None
    
    def create_lookup_type(self, name, description=None):
        """Create a new lookup type"""
        try:
            from datetime import datetime
            now = datetime.now()
            query = LookupQueryHelper.create_lookup_type_query(
                name=name, description=description, created_at=now
            )
            type_id = self.db_manager.execute_insert(query)
            
            return LookupType(id=type_id, name=name, description=description, created_at=now)
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error creating lookup type - name={name}, error={str(e)}")
            raise
    
    def create_lookup_value(self, lookup_type_id, code, value, description=None, sort_order=0):
        """Create a new lookup value"""
        try:
            from datetime import datetime
            now = datetime.now()
            query = LookupQueryHelper.create_lookup_value_query(
                lookup_type_id=lookup_type_id, code=code, value=value, 
                description=description, is_active=1, sort_order=sort_order, 
                created_at=now
            )
            value_id = self.db_manager.execute_insert(query)
            
            return LookupValue(
                id=value_id, lookup_type_id=lookup_type_id, code=code, 
                value=value, description=description, is_active=1, 
                sort_order=sort_order, created_at=now
            )
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error creating lookup value - code={code}, error={str(e)}")
            raise
    
    def update_lookup_type(self, type_id, name=None, description=None):
        """Update lookup type"""
        try:
            query = LookupQueryHelper.update_lookup_type_query(name=name, description=description, type_id=type_id)
            self.db_manager.execute_update(query)
            return True
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error updating lookup type - type_id={type_id}, error={str(e)}")
            return False
    
    def update_lookup_value(self, value_id, code=None, value=None, description=None, is_active=None, sort_order=None):
        """Update lookup value"""
        try:
            query = LookupQueryHelper.update_lookup_value_query(code=code, value=value, description=description, is_active=is_active, sort_order=sort_order, value_id=value_id)
            self.db_manager.execute_update(query)
            return True
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error updating lookup value - value_id={value_id}, error={str(e)}")
            return False
    
    def delete_lookup_type(self, type_id):
        """Delete lookup type"""
        try:
            query = LookupQueryHelper.delete_lookup_type_query(type_id=type_id)
            self.db_manager.execute_update(query)
            return True
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error deleting lookup type - type_id={type_id}, error={str(e)}")
            return False
    
    def delete_lookup_value(self, value_id):
        """Delete lookup value"""
        try:
            query = LookupQueryHelper.delete_lookup_value_query(value_id=value_id)
            self.db_manager.execute_update(query)
            return True
            
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error deleting lookup value - value_id={value_id}, error={str(e)}")
            return False
    
    def look_up(self, type_name):
        """Get lookup values by type name - main method for backward compatibility"""
        return self.get_lookup_values_by_type_name(type_name)
    
    def update_lookup_value_by_type_and_code(self, lookup_type_id, code, value_data):
        """Update lookup value by type ID and code"""
        try:
            query = LookupQueryHelper.update_lookup_value_by_type_and_code_query(
                value=value_data['value'],
                description=value_data.get('description'),
                is_active=value_data.get('is_active', True),
                sort_order=value_data.get('sort_order', 0),
                lookup_type_id=lookup_type_id,
                code=code
            )
            self.db_manager.execute_update(query)
            return True
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error updating lookup value by type and code - type_id={lookup_type_id}, code={code}, error={str(e)}")
            return False
    
    def delete_lookup_value_by_type_and_code(self, lookup_type_id, code):
        """Delete lookup value by type ID and code"""
        try:
            query = LookupQueryHelper.delete_lookup_value_by_type_and_code_query(lookup_type_id=lookup_type_id, code=code)
            self.db_manager.execute_update(query)
            return True
        except Exception as e:
            logging.error(f"LOOKUP_DAO: Error deleting lookup value by type and code - type_id={lookup_type_id}, code={code}, error={str(e)}")
            return False