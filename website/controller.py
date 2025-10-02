from fastapi import HTTPException
import logging

from website.website_models import ContactUs, PricingPlan
from website.dao import ContactUsDAO, PricingPlanDAO
from logical.email_service import send_contact_us_notification, send_contact_us_confirmation


class WebsiteController:
    """Controller for website business logic"""
    
    def __init__(self):
        self.contact_dao = ContactUsDAO()
        self.pricing_dao = PricingPlanDAO()
    
    def submit_contact_us(self, name, email, phone=None, whatsappNumber=None, message=""):
        """Submit a contact us form"""
        try:
            contact = self.contact_dao.create_contact_us(
                name=name, email=email, phone=phone, whatsappNumber=whatsappNumber, message=message
            )
            logging.info(f"WEBSITE_CONTROLLER: Contact us submitted successfully - contact_id={contact.id}, email={email}")
            
            # Prepare contact data for email
            contact_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'whatsappNumber': whatsappNumber,
                'message': message
            }
            
            # Send notification email to admin (optional - you can configure admin email)
            send_contact_us_notification(contact_data, "mhdali.kseekers@gmail.com")
            
            # Send confirmation email to the user
            send_contact_us_confirmation(contact_data)
            
            return contact
        except Exception as e:
            logging.error(f"WEBSITE_CONTROLLER: Contact us submission failed - email={email}, error={str(e)}")
            raise
    
    
    def get_pricing_plans(self, is_active=True):
        """Get all pricing plans"""
        try:
            plans = self.pricing_dao.get_all_pricing_plans(is_active=is_active)
            logging.info(f"WEBSITE_CONTROLLER: Retrieved {len(plans)} pricing plans")
            return plans
        except Exception as e:
            logging.error(f"WEBSITE_CONTROLLER: Error getting pricing plans - error={str(e)}")
            raise
    
