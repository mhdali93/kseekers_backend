import logging

class LookupQueryHelper:
    """Query helper for lookup module - Raw SQL queries"""
    
    
    @staticmethod
    def get_lookup_types_query():
        """Get SQL query for all lookup types"""
        return "SELECT * FROM lookup_types ORDER BY name"
    
    @staticmethod
    def get_lookup_type_by_name_query():
        """Get SQL query for lookup type by name"""
        return "SELECT * FROM lookup_types WHERE name = %s LIMIT 1"
    
    @staticmethod
    def get_lookup_values_by_type_id_query():
        """Get SQL query for lookup values by type ID"""
        return """
            SELECT * FROM lookup_values 
            WHERE lookup_type_id = %s AND is_active = 1
            ORDER BY sort_order, value
        """
    
    @staticmethod
    def get_lookup_values_by_type_name_query():
        """Get SQL query for lookup values by type name"""
        return """
            SELECT lv.* FROM lookup_values lv
            JOIN lookup_types lt ON lv.lookup_type_id = lt.id
            WHERE lt.name = %s AND lv.is_active = 1
            ORDER BY lv.sort_order, lv.value
        """
    
    @staticmethod
    def create_lookup_type_query():
        """Get SQL query to create a new lookup type"""
        return """
            INSERT INTO lookup_types (name, description, created_at)
            VALUES (%s, %s, %s)
        """
    
    @staticmethod
    def create_lookup_value_query():
        """Get SQL query to create a new lookup value"""
        return """
            INSERT INTO lookup_values (lookup_type_id, code, value, description, is_active, sort_order, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def get_lookup_value_by_id_query():
        """Get SQL query for lookup value by ID"""
        return "SELECT * FROM lookup_values WHERE id = %s LIMIT 1"
    
    @staticmethod
    def update_lookup_type_query():
        """Get SQL query to update lookup type"""
        return """
            UPDATE lookup_types 
            SET name = %s, description = %s
            WHERE id = %s
        """
    
    @staticmethod
    def update_lookup_value_query():
        """Get SQL query to update lookup value"""
        return """
            UPDATE lookup_values 
            SET code = %s, value = %s, description = %s, is_active = %s, sort_order = %s
            WHERE id = %s
        """
    
    @staticmethod
    def delete_lookup_type_query():
        """Get SQL query to delete lookup type"""
        return "DELETE FROM lookup_types WHERE id = %s"
    
    @staticmethod
    def delete_lookup_value_query():
        """Get SQL query to delete lookup value"""
        return "DELETE FROM lookup_values WHERE id = %s"
    
    @staticmethod
    def update_lookup_value_by_type_and_code_query():
        """Get SQL query to update lookup value by type ID and code"""
        return """
            UPDATE lookup_values 
            SET value = %s, description = %s, is_active = %s, sort_order = %s
            WHERE lookup_type_id = %s AND code = %s
        """
    
    @staticmethod
    def delete_lookup_value_by_type_and_code_query():
        """Get SQL query to delete lookup value by type ID and code"""
        return "DELETE FROM lookup_values WHERE lookup_type_id = %s AND code = %s"
    
