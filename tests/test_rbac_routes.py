"""
Unit tests for RBAC routes
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime

class TestRBACRoutes:
    """Test cases for RBAC routes"""
    
    def test_create_role_success(self, client, mock_role_data, auth_headers):
        """Test successful role creation"""
        with patch('rbac.controller.RBACController.create_role') as mock_create_role:
            mock_create_role.return_value = mock_role_data
            
            role_data = {
                "name": "test_role",
                "display_name": "Test Role",
                "description": "Test role description"
            }
            
            response = client.post("/rbac/roles/create", json=role_data, headers=auth_headers)
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["result"]["payload"]["name"] == "test_role"
    
    def test_create_role_validation_error(self, client, auth_headers):
        """Test role creation with validation error"""
        role_data = {
            "name": "",  # Invalid empty name
            "display_name": "Test Role"
        }
        
        response = client.post("/rbac/roles/create", json=role_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_create_role_unauthorized(self, client):
        """Test role creation without authentication"""
        role_data = {
            "name": "test_role",
            "display_name": "Test Role"
        }
        
        response = client.post("/rbac/roles/create", json=role_data)
        assert response.status_code == 403
    
    def test_list_roles_success(self, client, mock_role_data, auth_headers):
        """Test successful role listing"""
        with patch('rbac.controller.RBACController.list_roles') as mock_list_roles:
            mock_list_roles.return_value = [mock_role_data]
            
            response = client.get("/rbac/roles/list", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["name"] == "test_role"
    
    def test_list_roles_with_filters(self, client, mock_role_data, auth_headers):
        """Test role listing with filters"""
        with patch('rbac.controller.RBACController.list_roles') as mock_list_roles:
            mock_list_roles.return_value = [mock_role_data]
            
            params = {
                "name": "test",
                "is_active": True
            }
            
            response = client.get("/rbac/roles/list", headers=auth_headers, params=params)
            assert response.status_code == 200
            mock_list_roles.assert_called_once_with(name="test", is_active=True)
    
    def test_list_roles_unauthorized(self, client):
        """Test role listing without authentication"""
        response = client.get("/rbac/roles/list")
        assert response.status_code == 403
    
    def test_edit_role_success(self, client, mock_role_data, auth_headers):
        """Test successful role editing"""
        with patch('rbac.controller.RBACController.edit_role') as mock_edit_role:
            mock_edit_role.return_value = mock_role_data
            
            role_data = {
                "id": 1,
                "name": "updated_role",
                "display_name": "Updated Role",
                "description": "Updated description"
            }
            
            response = client.post("/rbac/roles/update", json=role_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["name"] == "test_role"
    
    def test_edit_role_validation_error(self, client, auth_headers):
        """Test role editing with validation error"""
        role_data = {
            "id": "invalid",  # Invalid ID type
            "name": "updated_role"
        }
        
        response = client.post("/rbac/roles/update", json=role_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_edit_role_unauthorized(self, client):
        """Test role editing without authentication"""
        role_data = {
            "id": 1,
            "name": "updated_role"
        }
        
        response = client.post("/rbac/roles/update", json=role_data)
        assert response.status_code == 403
    
    def test_create_right_success(self, client, mock_right_data, auth_headers):
        """Test successful right creation"""
        with patch('rbac.controller.RBACController.create_right') as mock_create_right:
            mock_create_right.return_value = mock_right_data
            
            right_data = {
                "name": "test_right",
                "display_name": "Test Right",
                "description": "Test right description",
                "resource_type": "api_endpoint",
                "resource_path": "/test",
                "http_method": "GET",
                "module": "test",
                "is_active": True
            }
            
            response = client.post("/rbac/rights/create", json=right_data, headers=auth_headers)
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["result"]["payload"]["name"] == "test_right"
    
    def test_create_right_validation_error(self, client, auth_headers):
        """Test right creation with validation error"""
        right_data = {
            "name": "",  # Invalid empty name
            "display_name": "Test Right",
            "resource_type": "invalid_type"  # Invalid resource type
        }
        
        response = client.post("/rbac/rights/create", json=right_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_create_right_unauthorized(self, client):
        """Test right creation without authentication"""
        right_data = {
            "name": "test_right",
            "display_name": "Test Right",
            "resource_type": "api_endpoint",
            "resource_path": "/test"
        }
        
        response = client.post("/rbac/rights/create", json=right_data)
        assert response.status_code == 403
    
    def test_list_rights_success(self, client, mock_right_data, auth_headers):
        """Test successful right listing"""
        with patch('rbac.controller.RBACController.list_rights') as mock_list_rights:
            mock_list_rights.return_value = [mock_right_data]
            
            response = client.get("/rbac/rights/list", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["name"] == "test_right"
    
    def test_list_rights_with_filters(self, client, mock_right_data, auth_headers):
        """Test right listing with filters"""
        with patch('rbac.controller.RBACController.list_rights') as mock_list_rights:
            mock_list_rights.return_value = [mock_right_data]
            
            params = {
                "name": "test",
                "is_active": True,
                "module": "test"
            }
            
            response = client.get("/rbac/rights/list", headers=auth_headers, params=params)
            assert response.status_code == 200
            mock_list_rights.assert_called_once_with(name="test", is_active=True, module="test")
    
    def test_list_rights_unauthorized(self, client):
        """Test right listing without authentication"""
        response = client.get("/rbac/rights/list")
        assert response.status_code == 403
    
    def test_edit_right_success(self, client, mock_right_data, auth_headers):
        """Test successful right editing"""
        with patch('rbac.controller.RBACController.edit_right') as mock_edit_right:
            mock_edit_right.return_value = mock_right_data
            
            right_data = {
                "id": 1,
                "name": "updated_right",
                "display_name": "Updated Right",
                "description": "Updated description"
            }
            
            response = client.post("/rbac/rights/update", json=right_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["name"] == "test_right"
    
    def test_edit_right_validation_error(self, client, auth_headers):
        """Test right editing with validation error"""
        right_data = {
            "id": "invalid",  # Invalid ID type
            "name": "updated_right"
        }
        
        response = client.post("/rbac/rights/update", json=right_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_edit_right_unauthorized(self, client):
        """Test right editing without authentication"""
        right_data = {
            "id": 1,
            "name": "updated_right"
        }
        
        response = client.post("/rbac/rights/update", json=right_data)
        assert response.status_code == 403
    
    def test_get_role_rights_success(self, client, mock_right_data, auth_headers):
        """Test successful role rights retrieval"""
        with patch('rbac.controller.RBACController.get_role_rights') as mock_get_role_rights:
            mock_get_role_rights.return_value = [mock_right_data]
            
            response = client.get("/rbac/role-rights/get/1", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["name"] == "test_right"
    
    def test_get_role_rights_unauthorized(self, client):
        """Test role rights retrieval without authentication"""
        response = client.get("/rbac/role-rights/get/1")
        assert response.status_code == 403
    
    def test_manage_role_rights_success(self, client, auth_headers):
        """Test successful role rights management"""
        with patch('rbac.controller.RBACController.manage_role_rights') as mock_manage_rights:
            mock_result = {
                "role_id": 1,
                "added": [1, 2],
                "removed": [3, 4]
            }
            mock_manage_rights.return_value = mock_result
            
            rights_data = {
                "role_id": 1,
                "right_ids": [1, 2, 5]
            }
            
            response = client.post("/rbac/role-rights/manage", json=rights_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["role_id"] == 1
            assert response_data["result"]["payload"]["added"] == [1, 2]
    
    def test_manage_role_rights_validation_error(self, client, auth_headers):
        """Test role rights management with validation error"""
        rights_data = {
            "role_id": "invalid",  # Invalid role ID type
            "right_ids": [1, 2]
        }
        
        response = client.post("/rbac/role-rights/manage", json=rights_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_manage_role_rights_unauthorized(self, client):
        """Test role rights management without authentication"""
        rights_data = {
            "role_id": 1,
            "right_ids": [1, 2]
        }
        
        response = client.post("/rbac/role-rights/manage", json=rights_data)
        assert response.status_code == 403
    
    def test_get_user_ui_rights_success(self, client, mock_right_data, auth_headers):
        """Test successful user UI rights retrieval"""
        with patch('rbac.controller.RBACController.get_user_ui_rights') as mock_get_ui_rights:
            mock_get_ui_rights.return_value = [mock_right_data]
            
            response = client.get("/rbac/user-rights/get/1", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["name"] == "test_right"
    
    def test_get_user_ui_rights_unauthorized(self, client):
        """Test user UI rights retrieval without authentication"""
        response = client.get("/rbac/user-rights/get/1")
        assert response.status_code == 403
    
    def test_check_user_api_access_success(self, client, auth_headers):
        """Test successful user API access check"""
        with patch('rbac.controller.RBACController.check_user_api_access') as mock_check_access:
            mock_result = {
                "user_id": 1,
                "api_path": "/test",
                "has_access": True,
                "rights": ["test_right"]
            }
            mock_check_access.return_value = mock_result
            
            access_data = {
                "user_id": 1,
                "api_path": "/test"
            }
            
            response = client.post("/rbac/user-api-access", json=access_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["user_id"] == 1
            assert response_data["result"]["payload"]["has_access"] == True
    
    def test_check_user_api_access_validation_error(self, client, auth_headers):
        """Test user API access check with validation error"""
        access_data = {
            "user_id": "invalid",  # Invalid user ID type
            "api_path": "/test"
        }
        
        response = client.post("/rbac/user-api-access", json=access_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_check_user_api_access_unauthorized(self, client):
        """Test user API access check without authentication"""
        access_data = {
            "user_id": 1,
            "api_path": "/test"
        }
        
        response = client.post("/rbac/user-api-access", json=access_data)
        assert response.status_code == 403
    
    def test_create_role_controller_exception(self, client, auth_headers):
        """Test role creation with controller exception"""
        with patch('rbac.controller.RBACController.create_role') as mock_create_role:
            mock_create_role.side_effect = Exception("Database error")
            
            role_data = {
                "name": "test_role",
                "display_name": "Test Role"
            }
            
            response = client.post("/rbac/roles/create", json=role_data, headers=auth_headers)
            assert response.status_code == 500
    
    def test_list_roles_controller_exception(self, client, auth_headers):
        """Test role listing with controller exception"""
        with patch('rbac.controller.RBACController.list_roles') as mock_list_roles:
            mock_list_roles.side_effect = Exception("Database error")
            
            response = client.get("/rbac/roles/list", headers=auth_headers)
            assert response.status_code == 500
