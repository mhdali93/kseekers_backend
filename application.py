import uvicorn
import os
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.exceptions import RequestValidationError
import config

from starlette.middleware.cors import CORSMiddleware

import logging
import sys
from logging.handlers import RotatingFileHandler

from datetime import datetime as dt

# Ensure the logs directory exists
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

#Routes
from routes.healthcheck_routes import HealthCheckRoutes
from look_up.routes import LookUpRoutes
from auth.routes import AuthRoutes
from display_config.routes import DisplayConfigRoutes
from rbac.routes import RBACRoutes
from users.routes import UserRoutes
from website.routes import WebsiteRoutes

# Exception handlers
from middlerware.custom_exception_handler import HTTPExceptionHandler, RequestValidationExceptionHandler

app = FastAPI(
    title="kseekers",
    version="0.0.1",
    description="Knack Seekers",
)

# Create a root logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of messages

# Standard formatter for logging calls
formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] - %(levelname)s : %(message)s')

try:
    file_handler = RotatingFileHandler(
        filename=config.logging_path
        , maxBytes=config.logging_file_size
        , backupCount=config.logging_backup_count
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
except Exception as logex:
    print(f"Error while setting logging file handler: {logex}")

logging.info('Application Started')
logging.error('Test Error Message')

# Cross-origin for Cors
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add exception handlers
app.add_exception_handler(HTTPException, HTTPExceptionHandler.handler)
app.add_exception_handler(RequestValidationError, RequestValidationExceptionHandler.handler)

# Initialize route instances
health_routes = HealthCheckRoutes()
lookup_routes = LookUpRoutes()
auth_routes = AuthRoutes()
display_config_routes = DisplayConfigRoutes()
rbac_routes = RBACRoutes()
user_routes = UserRoutes()
website_routes = WebsiteRoutes()

# Include routers
app.include_router(health_routes.app, tags=["HEALTH CHECK"])
app.include_router(lookup_routes.app)
app.include_router(auth_routes.app)
app.include_router(display_config_routes.app)
app.include_router(rbac_routes.app)
app.include_router(user_routes.app)
app.include_router(website_routes.app)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8006
    )
