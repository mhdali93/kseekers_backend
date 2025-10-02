"""
Unit tests for user management routes
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime

class TestUserRoutes:
    """Test cases for user management routes"""
    
    def test_list_users_success(self, client, mock_user_data, auth_headers):
        """Test successful user listing"""
        with patch('users.controller.UserController.list_users') as mock_list_users:
            # Create a proper mock User object with string dates
            mock_user = Mock()
            mock_user.to_dict.return_value = mock_user_data
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.email = "test@example.com"
            
            mock_list_users.return_value = ([mock_user], 1)
            
            response = client.get("/users/list", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            # Check the wrapped response format
            assert "result" in response_data
            assert response_data["result"]["payload"]["users"][0]["id"] == 1
            assert response_data["result"]["payload"]["users"][0]["username"] == "testuser"
            assert response_data["result"]["payload"]["total"] == 1
    
    def test_list_users_with_filters(self, client, mock_user_data, auth_headers):
        """Test user listing with filters"""
        with patch('users.controller.UserController.list_users') as mock_list_users:
            mock_user = Mock()
            mock_user.to_dict.return_value = mock_user_data
            mock_list_users.return_value = ([mock_user], 1)
            
            params = {
                "page": 1,
                "per_page": 10,
                "search": "test",
                "is_active": True,
                "role_id": 1
            }
            
            response = client.get("/users/list", headers=auth_headers, params=params)
            assert response.status_code == 200
            mock_list_users.assert_called_once_with(1, 10, "test", True, 1)
    
    def test_list_users_unauthorized(self, client):
        """Test user listing without authentication"""
        response = client.get("/users/list")
        assert response.status_code == 403  # Forbidden (actual API behavior)
    
    def test_create_user_success(self, client, mock_user_data, auth_headers):
        """Test successful user creation"""
        with patch('users.controller.UserController.create_user') as mock_create_user:
            mock_user = Mock()
            # Create mock data that matches what should be returned
            mock_user_data_created = {
                "id": 1,
                "username": "newuser",
                "email": "newuser@example.com",
                "phone": "9876543210",
                "is_active": True,
                "is_admin": False,
                "role_id": 1,
                "created_at": mock_user_data["created_at"],
                "updated_at": mock_user_data["updated_at"]
            }
            mock_user.to_dict.return_value = mock_user_data_created
            mock_create_user.return_value = mock_user
            
            user_data = {
                "username": "newuser",
                "email": "newuser@example.com",
                "phone": "9876543210",
                "is_active": True,
                "is_admin": False,
                "role_id": 1
            }
            
            response = client.post("/users/create", json=user_data, headers=auth_headers)
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["result"]["payload"]["id"] == 1
            assert response_data["result"]["payload"]["username"] == "newuser"
    
    def test_create_user_validation_error(self, client, auth_headers):
        """Test user creation with validation error"""
        user_data = {
            "username": "",  # Invalid empty username
            "email": "invalid-email",  # Invalid email format
        }
        
        response = client.post("/users/create", json=user_data, headers=auth_headers)
        assert response.status_code == 400  # Bad Request (actual API behavior)
    
    def test_create_user_unauthorized(self, client):
        """Test user creation without authentication"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com"
        }
        
        response = client.post("/users/create", json=user_data)
        assert response.status_code == 403  # Forbidden (actual API behavior)
    
    def test_get_user_success(self, client, mock_user_data, auth_headers):
        """Test successful user retrieval by ID"""
        with patch('users.controller.UserController.get_user') as mock_get_user:
            mock_user = Mock()
            mock_user.to_dict.return_value = mock_user_data
            mock_get_user.return_value = mock_user
            
            response = client.get("/users/get/1", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["id"] == 1
            assert response_data["result"]["payload"]["username"] == "testuser"
    
    def test_get_user_not_found(self, client, auth_headers):
        """Test user retrieval when user not found"""
        with patch('users.controller.UserController.get_user') as mock_get_user:
            mock_get_user.return_value = None
            
            response = client.get("/users/get/999", headers=auth_headers)
            assert response.status_code == 404
    
    def test_get_user_unauthorized(self, client):
        """Test user retrieval without authentication"""
        response = client.get("/users/get/1")
        assert response.status_code == 403  # Forbidden (actual API behavior)
    
    def test_update_user_success(self, client, mock_user_data, auth_headers):
        """Test successful user update"""
        with patch('users.controller.UserController.update_user') as mock_update_user:
            mock_user = Mock()
            mock_user.to_dict.return_value = mock_user_data
            mock_update_user.return_value = mock_user
            
            user_data = {
                "user_id": 1,
                "username": "updateduser",
                "email": "updated@example.com",
                "phone": "1111111111"
            }
            
            response = client.post("/users/update", json=user_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["id"] == 1
    
    def test_update_user_not_found(self, client, auth_headers):
        """Test user update when user not found"""
        with patch('users.controller.UserController.update_user') as mock_update_user:
            from fastapi import HTTPException
            mock_update_user.side_effect = HTTPException(status_code=404, detail="User not found")
            
            user_data = {
                "user_id": 999,
                "username": "updateduser"
            }
            
            response = client.post("/users/update", json=user_data, headers=auth_headers)
            assert response.status_code == 404
    
    def test_update_user_unauthorized(self, client):
        """Test user update without authentication"""
        user_data = {
            "user_id": 1,
            "username": "updateduser"
        }
        
        response = client.post("/users/update", json=user_data)
        assert response.status_code == 403  # Forbidden (actual API behavior)
    
    def test_get_user_rights_success(self, client, mock_user_data, mock_right_data, auth_headers):
        """Test successful user rights retrieval"""
        with patch('users.controller.UserController.get_user') as mock_get_user, \
             patch('users.controller.UserController.get_user_rights') as mock_get_rights:
            
            mock_user = Mock()
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.role_id = 1
            mock_get_user.return_value = mock_user
            
            mock_right = Mock()
            mock_right.id = 1
            mock_right.name = "test_right"
            mock_right.display_name = "Test Right"
            mock_right.description = "Test right description"
            mock_right.resource_type = "api_endpoint"
            mock_right.resource_path = "/test"
            mock_right.http_method = "GET"
            mock_right.module = "test"
            mock_right.is_active = True
            mock_get_rights.return_value = [mock_right]
            
            response = client.get("/users/rights/1", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["user_id"] == 1
            assert response_data["result"]["payload"]["username"] == "testuser"
            assert len(response_data["result"]["payload"]["rights"]) == 1
    
    def test_get_user_rights_with_filters(self, client, mock_user_data, auth_headers):
        """Test user rights retrieval with filters"""
        with patch('users.controller.UserController.get_user') as mock_get_user, \
             patch('users.controller.UserController.get_user_rights') as mock_get_rights:
            
            mock_user = Mock()
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.role_id = 1
            mock_get_user.return_value = mock_user
            mock_get_rights.return_value = []
            
            params = {
                "resource_type": "api_endpoint",
                "module": "test"
            }
            
            response = client.get("/users/rights/1", headers=auth_headers, params=params)
            assert response.status_code == 200
            mock_get_rights.assert_called_once_with(1, "api_endpoint", "test")
    
    def test_get_user_rights_user_not_found(self, client, auth_headers):
        """Test user rights retrieval when user not found"""
        with patch('users.controller.UserController.get_user') as mock_get_user:
            mock_get_user.return_value = None
            
            response = client.get("/users/rights/999", headers=auth_headers)
            assert response.status_code == 404
    
    def test_check_user_api_access_success(self, client, auth_headers):
        """Test successful API access check"""
        with patch('users.controller.UserController.check_user_api_access') as mock_check_access:
            mock_result = {
                "user_id": 1,
                "api_path": "/test",
                "has_access": True,
                "rights": ["test_right"]
            }
            mock_check_access.return_value = mock_result
            
            access_data = {
                "user_id": 1,
                "resource_path": "/test",
                "http_method": "GET"
            }
            
            response = client.post("/users/api-access", json=access_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["user_id"] == 1
            assert response_data["result"]["payload"]["has_access"] == True
    
    def test_check_user_api_access_unauthorized(self, client):
        """Test API access check without authentication"""
        access_data = {
            "user_id": 1,
            "resource_path": "/test"
        }
        
        response = client.post("/users/api-access", json=access_data)
        assert response.status_code == 403  # Forbidden (actual API behavior)
    
    def test_list_users_controller_exception(self, client, auth_headers):
        """Test user listing with controller exception"""
        with patch('users.controller.UserController.list_users') as mock_list_users:
            mock_list_users.side_effect = Exception("Database error")
            
            response = client.get("/users/list", headers=auth_headers)
            assert response.status_code == 500
    
    def test_create_user_controller_exception(self, client, auth_headers):
        """Test user creation with controller exception"""
        with patch('users.controller.UserController.create_user') as mock_create_user:
            mock_create_user.side_effect = Exception("Database error")
            
            user_data = {
                "username": "newuser",
                "email": "newuser@example.com"
            }
            
            response = client.post("/users/create", json=user_data, headers=auth_headers)
            assert response.status_code == 500
