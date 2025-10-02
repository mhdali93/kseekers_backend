from fastapi import APIRouter, HTTPException, Depends, Request, Query
from utils.decorator import DecoratorUtils

from website.website_schemas import (
    ContactUsRequest, ContactUsResponse, PricingPlanResponse, 
    MessageResponse
)
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, ExceptionMessage, UniversalMessage
from website.controller import WebsiteController
from logical.logger import log_request, update_log

import logging

class WebsiteRoutes:
    """Website routes for contact us and pricing plans"""
    
    def __init__(self):
        self.app = APIRouter(prefix="/website", tags=["Website"])
        self.controller = WebsiteController()
        self.__add_routes()
    
    def __add_routes(self):
        # Contact Us route
        self.app.add_api_route(
            path="/contact-us",
            endpoint=self.submit_contact_us,
            methods=["POST"]
        )
        
        # Pricing Plans route
        self.app.add_api_route(
            path="/pricing-plans",
            endpoint=self.get_pricing_plans,
            methods=["GET"]
        )
    
    @DecoratorUtils.create_endpoint(
        success_message="Contact form submitted successfully",
        error_message="Error submitting contact form",
        success_status=HTTPStatus.created
    )
    async def submit_contact_us(self, request: Request, contact_data: ContactUsRequest,
                               logger: str = Query(None, include_in_schema=False)):
        """Submit a contact us form"""
        contact = self.controller.submit_contact_us(
            name=contact_data.name,
            email=contact_data.email,
            phone=contact_data.phone,
            whatsappNumber=contact_data.whatsappNumber,
            message=contact_data.message
        )
        
        return {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "whatsappNumber": contact.whatsappNumber,
            "message": contact.message,
            "created_at": contact.created_at.isoformat()
        }
    
    
    @DecoratorUtils.create_endpoint(
        success_message="Pricing plans retrieved successfully",
        error_message="Error retrieving pricing plans"
    )
    async def get_pricing_plans(self, request: Request,
                               is_active: bool = Query(True),
                               logger: str = Query(None, include_in_schema=False)):
        """Get all pricing plans"""
        plans = self.controller.get_pricing_plans(is_active=is_active)
        
        plan_responses = []
        for plan in plans:
            plan_responses.append({
                "id": plan.id,
                "title": plan.title,
                "sessions": plan.sessions,
                "duration": plan.duration,
                "basePrice": plan.base_price,
                "retentionDiscount": plan.retention_discount,
                "freeSessions": plan.free_sessions,
                "curriculum": plan.curriculum,
                "features": plan.features,
                "current": plan.is_current,
                "popular": plan.is_popular,
                "is_active": plan.is_active
            })
        
        return plan_responses
    
