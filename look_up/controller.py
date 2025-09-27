import traceback
import logging
from fastapi.encoders import jsonable_encoder
from look_up.dao import LookUpDao


class LookUpController:
    def __init__(self):
        self.dao = LookUpDao()

    def get_headers_info(self, header_type):
        try:
            headers = self.dao.look_up(header_type)
            logging.info(f"Lookup Headers: {headers}")
            if headers:
                headers = jsonable_encoder(headers)
                logging.info(f'Got Headers length {len(headers)}')
                response = headers

            else:
                response = None

            return response

        except Exception as e:
            logging.error("Inside Exception Block get_headers_info")
            traceback.print_tb(e.__traceback__)
            raise e
    
    def get_lookup_types(self):
        """Get all lookup types"""
        try:
            return self.dao.get_lookup_types()
        except Exception as e:
            logging.error(f"Error in get_lookup_types: {e}")
            raise e
    
    def get_lookup_values_by_type_name(self, type_name):
        """Get lookup values by type name"""
        try:
            return self.dao.get_lookup_values_by_type_name(type_name)
        except Exception as e:
            logging.error(f"Error in get_lookup_values_by_type_name: {e}")
            raise e
    
    def get_lookup_values_by_type_id(self, type_id):
        """Get lookup values by type ID"""
        try:
            return self.dao.get_lookup_values_by_type_id(type_id)
        except Exception as e:
            logging.error(f"Error in get_lookup_values_by_type_id: {e}")
            raise e
    
    def get_lookup_type_by_name(self, name):
        """Get lookup type by name"""
        try:
            return self.dao.get_lookup_type_by_name(name)
        except Exception as e:
            logging.error(f"Error in get_lookup_type_by_name: {e}")
            raise e
    
    def get_lookup_value_by_id(self, value_id):
        """Get lookup value by ID"""
        try:
            return self.dao.get_lookup_value_by_id(value_id)
        except Exception as e:
            logging.error(f"Error in get_lookup_value_by_id: {e}")
            raise e
    
    def create_lookup_type(self, name, description=None):
        """Create a new lookup type"""
        try:
            return self.dao.create_lookup_type(name, description)
        except Exception as e:
            logging.error(f"Error in create_lookup_type: {e}")
            raise e
    
    def create_lookup_value(self, lookup_type_id, code, value, description=None, is_active=True, sort_order=0):
        """Create a new lookup value"""
        try:
            return self.dao.create_lookup_value(lookup_type_id, code, value, description, is_active, sort_order)
        except Exception as e:
            logging.error(f"Error in create_lookup_value: {e}")
            raise e
    
    def update_lookup_type(self, type_id, name=None, description=None):
        """Update lookup type"""
        try:
            return self.dao.update_lookup_type(type_id, name, description)
        except Exception as e:
            logging.error(f"Error in update_lookup_type: {e}")
            raise e
    
    def update_lookup_value(self, value_id, code=None, value=None, description=None, is_active=None, sort_order=None):
        """Update lookup value"""
        try:
            return self.dao.update_lookup_value(value_id, code, value, description, is_active, sort_order)
        except Exception as e:
            logging.error(f"Error in update_lookup_value: {e}")
            raise e
    
    def delete_lookup_type(self, type_id):
        """Delete lookup type"""
        try:
            return self.dao.delete_lookup_type(type_id)
        except Exception as e:
            logging.error(f"Error in delete_lookup_type: {e}")
            raise e
    
    def delete_lookup_value(self, value_id):
        """Delete lookup value"""
        try:
            return self.dao.delete_lookup_value(value_id)
        except Exception as e:
            logging.error(f"Error in delete_lookup_value: {e}")
            raise e