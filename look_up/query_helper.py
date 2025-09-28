import logging

class LookupQueryHelper:
    """Query helper for lookup module - Raw SQL queries"""
    
    @staticmethod
    def _convert_boolean_to_int(value):
        """Convert boolean values to integers for database storage"""
        if isinstance(value, bool):
            return 1 if value else 0
        return value
    
    
    @staticmethod
    def get_lookup_types_query():
        """Get SQL query for all lookup types"""
        query = "SELECT * FROM lookup_types ORDER BY name"
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - get_lookup_types_query: {query}")
        return query
    
    @staticmethod
    def get_lookup_type_by_name_query(name=None):
        """Get SQL query for lookup type by name with values formatted"""
        if name is None:
            raise ValueError("name is required for get_lookup_type_by_name_query")
        
        query = f"SELECT * FROM lookup_types WHERE name = '{name}' LIMIT 1"
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - get_lookup_type_by_name_query: {query}")
        return query
    
    @staticmethod
    def get_lookup_values_by_type_id_query(lookup_type_id=None):
        """Get SQL query for lookup values by type ID with values formatted"""
        if lookup_type_id is None:
            raise ValueError("lookup_type_id is required for get_lookup_values_by_type_id_query")
        
        query = f"""
            SELECT * FROM lookup_values 
            WHERE lookup_type_id = {lookup_type_id} AND is_active = 1
            ORDER BY sort_order, value
        """
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - get_lookup_values_by_type_id_query: {query}")
        return query
    
    @staticmethod
    def get_lookup_values_by_type_name_query(type_name=None):
        """Get SQL query for lookup values by type name with values formatted"""
        if type_name is None:
            raise ValueError("type_name is required for get_lookup_values_by_type_name_query")
        
        query = f"""
            SELECT lv.* FROM lookup_values lv
            JOIN lookup_types lt ON lv.lookup_type_id = lt.id
            WHERE lt.name = '{type_name}' AND lv.is_active = 1
            ORDER BY lv.sort_order, lv.value
        """
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - get_lookup_values_by_type_name_query: {query}")
        return query
    
    @staticmethod
    def create_lookup_type_query(name=None, description=None, created_at=None):
        """Get SQL query to create a new lookup type with values directly bound"""
        if name is None:
            raise ValueError("name is required for create_lookup_type_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['name']
        values = [f"'{name}'"]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if description is not None:
            columns.append('description')
            values.append(f"'{description}'")
        if created_at is not None:
            columns.append('created_at')
            values.append(f"'{created_at}'")
        
        # Create query with values directly bound
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        
        query = f"INSERT INTO lookup_types ({columns_str}) VALUES ({values_str})"
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - create_lookup_type_query: {query}")
        return query
    
    @staticmethod
    def create_lookup_value_query(lookup_type_id=None, code=None, value=None, description=None, is_active=None, sort_order=None, created_at=None):
        """Get SQL query to create a new lookup value with values directly bound"""
        if lookup_type_id is None:
            raise ValueError("lookup_type_id is required for create_lookup_value_query")
        if code is None:
            raise ValueError("code is required for create_lookup_value_query")
        if value is None:
            raise ValueError("value is required for create_lookup_value_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['lookup_type_id', 'code', 'value']
        values = [str(lookup_type_id), f"'{code}'", f"'{value}'"]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if description is not None:
            columns.append('description')
            values.append(f"'{description}'")
        if is_active is not None:
            columns.append('is_active')
            values.append(str(LookupQueryHelper._convert_boolean_to_int(is_active)))
        if sort_order is not None:
            columns.append('sort_order')
            values.append(str(sort_order))
        if created_at is not None:
            columns.append('created_at')
            values.append(f"'{created_at}'")
        
        # Create query with values directly bound
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        
        query = f"INSERT INTO lookup_values ({columns_str}) VALUES ({values_str})"
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - create_lookup_value_query: {query}")
        return query
    
    @staticmethod
    def get_lookup_value_by_id_query(value_id=None):
        """Get SQL query for lookup value by ID with values formatted"""
        if value_id is None:
            raise ValueError("value_id is required for get_lookup_value_by_id_query")
        
        query = f"SELECT * FROM lookup_values WHERE id = {value_id} LIMIT 1"
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - get_lookup_value_by_id_query: {query}")
        return query
    
    @staticmethod
    def update_lookup_type_query(name=None, description=None, type_id=None):
        """Get SQL query to update lookup type with values formatted"""
        if name is None:
            raise ValueError("name is required for update_lookup_type_query")
        if type_id is None:
            raise ValueError("type_id is required for update_lookup_type_query")
        
        query = f"""
            UPDATE lookup_types 
            SET name = '{name}', description = '{description}'
            WHERE id = {type_id}
        """
        logging.info(f"LOOKUP_QUERY_HELPER: Generated query - update_lookup_type_query: {query}")
        return query
    
    @staticmethod
    def update_lookup_value_query(code=None, value=None, description=None, is_active=None, sort_order=None, value_id=None):
        """Get SQL query to update lookup value with values formatted"""
        if code is None:
            raise ValueError("code is required for update_lookup_value_query")
        if value is None:
            raise ValueError("value is required for update_lookup_value_query")
        if is_active is None:
            raise ValueError("is_active is required for update_lookup_value_query")
        if value_id is None:
            raise ValueError("value_id is required for update_lookup_value_query")
        
        return f"""
            UPDATE lookup_values 
            SET code = '{code}', value = '{value}', description = '{description}', is_active = {is_active}, sort_order = {sort_order}
            WHERE id = {value_id}
        """
    
    @staticmethod
    def delete_lookup_type_query(type_id=None):
        """Get SQL query to delete lookup type with values formatted"""
        if type_id is None:
            raise ValueError("type_id is required for delete_lookup_type_query")
        
        return f"DELETE FROM lookup_types WHERE id = {type_id}"
    
    @staticmethod
    def delete_lookup_value_query(value_id=None):
        """Get SQL query to delete lookup value with values formatted"""
        if value_id is None:
            raise ValueError("value_id is required for delete_lookup_value_query")
        
        return f"DELETE FROM lookup_values WHERE id = {value_id}"
    
    @staticmethod
    def update_lookup_value_by_type_and_code_query(value=None, description=None, is_active=None, sort_order=None, lookup_type_id=None, code=None):
        """Get SQL query to update lookup value by type ID and code with values formatted"""
        if value is None:
            raise ValueError("value is required for update_lookup_value_by_type_and_code_query")
        if is_active is None:
            raise ValueError("is_active is required for update_lookup_value_by_type_and_code_query")
        if lookup_type_id is None:
            raise ValueError("lookup_type_id is required for update_lookup_value_by_type_and_code_query")
        if code is None:
            raise ValueError("code is required for update_lookup_value_by_type_and_code_query")
        
        return f"""
            UPDATE lookup_values 
            SET value = '{value}', description = '{description}', is_active = {is_active}, sort_order = {sort_order}
            WHERE lookup_type_id = {lookup_type_id} AND code = '{code}'
        """
    
    @staticmethod
    def delete_lookup_value_by_type_and_code_query(lookup_type_id=None, code=None):
        """Get SQL query to delete lookup value by type ID and code with values formatted"""
        if lookup_type_id is None:
            raise ValueError("lookup_type_id is required for delete_lookup_value_by_type_and_code_query")
        if code is None:
            raise ValueError("code is required for delete_lookup_value_by_type_and_code_query")
        
        return f"DELETE FROM lookup_values WHERE lookup_type_id = {lookup_type_id} AND code = '{code}'"
    
