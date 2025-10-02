import json
import logging
from datetime import datetime

from manager.db_manager import DBManager
from website.website_models import ContactUs, PricingPlan
from website.query_helper import WebsiteQueryHelper
from utils.decorator import DecoratorUtils

class ContactUsDAO:
    """Data Access Object for Contact Us operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    def create_contact_us(self, name, email, phone=None, whatsappNumber=None, message=""):
        """Create a new contact us record"""
        try:
            now = datetime.now()
            query = WebsiteQueryHelper.create_contact_us_query(
                name=name, email=email, phone=phone, whatsappNumber=whatsappNumber, 
                message=message, created_at=now, updated_at=now
            )
            contact_id = self.db_manager.execute_insert(query)
            logging.info(f"CONTACT_US_DAO: Contact us record created - contact_id={contact_id}, email={email}")
            
            return ContactUs(id=contact_id, name=name, email=email, phone=phone, 
                           whatsappNumber=whatsappNumber, message=message)
        except Exception as e:
            logging.error(f"CONTACT_US_DAO: Contact us creation failed - email={email}, error={str(e)}")
            raise
    


class PricingPlanDAO:
    """Data Access Object for Pricing Plan operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    @DecoratorUtils.profile
    def get_all_pricing_plans(self, is_active=True):
        """Get all pricing plans with optional filtering"""
        try:
            query = WebsiteQueryHelper.get_all_pricing_plans_query(is_active=is_active)
            result = self.db_manager.execute_query(query)
            
            plans = []
            if result:
                for row in result:
                    plan = PricingPlan.from_dict(row)
                    plans.append(plan)
            
            return plans
        except Exception as e:
            logging.error(f"PRICING_PLAN_DAO: Error getting pricing plans - error={str(e)}")
            raise
    
