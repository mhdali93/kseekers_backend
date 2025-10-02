"""
Pytest configuration and fixtures for KSeekers API tests
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application import app
from logical.jwt_auth import JWTHandler

# Test client fixture
@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)

# Mock database manager
@pytest.fixture
def mock_db_manager():
    """Mock database manager for testing"""
    mock_db = Mock()
    mock_db.execute_query.return_value = []
    mock_db.execute_insert.return_value = 1
    mock_db.execute_update.return_value = True
    return mock_db

# Mock JWT token
@pytest.fixture
def mock_jwt_token():
    """Create a mock JWT token for testing"""
    jwt_handler = JWTHandler()
    return jwt_handler.create_token(
        user_id=1,
        username="testuser",
        is_admin=False
    )

# Mock authentication headers
@pytest.fixture
def auth_headers(mock_jwt_token):
    """Create authentication headers for testing"""
    return {"Authorization": f"Bearer {mock_jwt_token}"}

# Mock user data
@pytest.fixture
def mock_user_data():
    """Mock user data for testing"""
    now = datetime.now()
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone": "1234567890",
        "is_active": True,
        "is_admin": False,
        "role_id": 1,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }

# Mock RBAC data
@pytest.fixture
def mock_role_data():
    """Mock role data for testing"""
    now = datetime.now()
    return {
        "id": 1,
        "name": "test_role",
        "display_name": "Test Role",
        "description": "Test role description",
        "is_active": True,
        "is_system_role": False,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }

@pytest.fixture
def mock_right_data():
    """Mock right data for testing"""
    now = datetime.now()
    return {
        "id": 1,
        "name": "test_right",
        "display_name": "Test Right",
        "description": "Test right description",
        "resource_type": "api_endpoint",
        "resource_path": "/test",
        "http_method": "GET",
        "module": "test",
        "is_active": True,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }

# Mock display config data
@pytest.fixture
def mock_grid_metadata_data():
    """Mock grid metadata data for testing"""
    now = datetime.now()
    return {
        "id": 1,
        "gridName": "test_grid",
        "gridNameId": "test_grid_001",
        "description": "Test grid metadata",
        "is_active": True,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }

@pytest.fixture
def mock_display_config_data():
    """Mock display config data for testing"""
    now = datetime.now()
    return {
        "id": 1,
        "gridNameId": "test_grid_001",
        "displayId": "test_display",
        "title": "Test Display",
        "hidden": False,
        "width": 100,
        "sortIndex": 1,
        "ellipsis": False,
        "align": "left",
        "dbDataType": "string",
        "codeDataType": "string",
        "format": None,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }

# Mock lookup data
@pytest.fixture
def mock_lookup_type_data():
    """Mock lookup type data for testing"""
    now = datetime.now()
    return {
        "id": 1,
        "name": "test_type",
        "description": "Test lookup type",
        "is_active": True,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }

@pytest.fixture
def mock_lookup_value_data():
    """Mock lookup value data for testing"""
    now = datetime.now()
    return {
        "id": 1,
        "lookup_type_id": 1,
        "code": "test_code",
        "value": "Test Value",
        "description": "Test lookup value",
        "is_active": True,
        "sort_order": 1,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }

# Mock request state
@pytest.fixture
def mock_request_state():
    """Mock request state for JWT authentication"""
    state = Mock()
    state.user_id = 1
    state.username = "testuser"
    return state

# Async test runner
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()