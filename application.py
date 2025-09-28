import uvicorn
import os
from fastapi import FastAPI
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

app.include_router(HealthCheckRoutes().app, tags=["HEALTH CHECK"])
app.include_router(LookUpRoutes().app)
app.include_router(AuthRoutes().app)
app.include_router(DisplayConfigRoutes().app)
app.include_router(RBACRoutes().app)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8006
    )
