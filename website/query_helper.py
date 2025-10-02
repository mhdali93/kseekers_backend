import logging

class WebsiteQueryHelper:
    """Query helper for website module - Raw SQL queries"""
    
    @staticmethod
    def _convert_boolean_to_int(value):
        """Convert boolean values to integers for database storage"""
        if isinstance(value, bool):
            return 1 if value else 0
        return value
    
    @staticmethod
    def create_contact_us_query(name=None, email=None, phone=None, whatsappNumber=None, message=None, 
                               created_at=None, updated_at=None):
        """Get SQL query to create a new contact us record with values directly bound"""
        if name is None:
            raise ValueError("name is required for create_contact_us_query")
        if email is None:
            raise ValueError("email is required for create_contact_us_query")
        if message is None:
            raise ValueError("message is required for create_contact_us_query")
        
        # Build dynamic column and value lists, skipping None values for columns with defaults
        columns = ['name', 'email', 'message']
        values = [f"'{name}'", f"'{email}'", f"'{message}'"]
        
        # Add optional columns only if they have values (skip None to use DB defaults)
        if phone is not None:
            columns.append('phone')
            values.append(f"'{phone}'")
        if whatsappNumber is not None:
            columns.append('whatsappNumber')
            values.append(f"'{whatsappNumber}'")
        if created_at is not None:
            columns.append('created_at')
            values.append(f"'{created_at}'")
        if updated_at is not None:
            columns.append('updated_at')
            values.append(f"'{updated_at}'")
        
        # Create query with values directly bound
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        
        query = f"INSERT INTO contact_us ({columns_str}) VALUES ({values_str})"
        logging.info(f"WEBSITE_QUERY_HELPER: Generated query - create_contact_us_query: {query}")
        return query
    
    
    @staticmethod
    def get_all_pricing_plans_query(is_active=None):
        """Get SQL query for all pricing plans with optional filtering"""
        query = "SELECT * FROM pricing_plans"
        
        conditions = []
        if is_active is not None:
            conditions.append(f"is_active = {WebsiteQueryHelper._convert_boolean_to_int(is_active)}")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY created_at ASC"
        
        logging.info(f"WEBSITE_QUERY_HELPER: Generated query - get_all_pricing_plans_query: {query}")
        return query
    
