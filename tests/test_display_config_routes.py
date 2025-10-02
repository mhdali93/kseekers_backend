"""
Unit tests for display config routes
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime

class TestDisplayConfigRoutes:
    """Test cases for display config routes"""
    
    def test_create_grid_metadata_success(self, client, mock_grid_metadata_data, auth_headers):
        """Test successful grid metadata creation"""
        with patch('display_config.controller.DisplayConfigController.create_grid_metadata') as mock_create:
            mock_create.return_value = 1
            
            grid_data = {
                "gridName": "test_grid",
                "gridNameId": "test_grid_001",
                "description": "Test grid metadata"
            }
            
            response = client.post("/display-config/grid-metadata/create", json=grid_data, headers=auth_headers)
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["result"]["payload"]["id"] == 1
    
    def test_create_grid_metadata_validation_error(self, client, auth_headers):
        """Test grid metadata creation with validation error"""
        grid_data = {
            "gridName": "",  # Invalid empty name
            "gridNameId": "test_grid_001"
        }
        
        response = client.post("/display-config/grid-metadata/create", json=grid_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_create_grid_metadata_unauthorized(self, client):
        """Test grid metadata creation without authentication"""
        grid_data = {
            "gridName": "test_grid",
            "gridNameId": "test_grid_001"
        }
        
        response = client.post("/display-config/grid-metadata/create", json=grid_data)
        assert response.status_code == 403
    
    def test_list_grid_metadata_success(self, client, mock_grid_metadata_data):
        """Test successful grid metadata listing"""
        with patch('display_config.controller.DisplayConfigController.list_grid_metadata') as mock_list:
            mock_list.return_value = [mock_grid_metadata_data]
            
            request_data = {
                "name": "test",
                "is_active": True
            }
            
            response = client.post("/display-config/grid-metadata/list", json=request_data)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["gridName"] == "test_grid"
    
    def test_list_grid_metadata_validation_error(self, client):
        """Test grid metadata listing with validation error"""
        request_data = {
            "name": 123,  # Invalid type
            "is_active": "invalid"  # Invalid type
        }
        
        response = client.post("/display-config/grid-metadata/list", json=request_data)
        assert response.status_code == 400
    
    def test_update_grid_metadata_success(self, client, auth_headers):
        """Test successful grid metadata update"""
        with patch('display_config.controller.DisplayConfigController.update_grid_metadata') as mock_update:
            mock_update.return_value = True
            
            update_data = {
                "id": 1,
                "gridName": "updated_grid",
                "description": "Updated description"
            }
            
            response = client.post("/display-config/grid-metadata/edit", json=update_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["id"] == 1
    
    def test_update_grid_metadata_not_found(self, client, auth_headers):
        """Test grid metadata update when not found"""
        with patch('display_config.controller.DisplayConfigController.update_grid_metadata') as mock_update:
            mock_update.return_value = False
            
            update_data = {
                "id": 999,
                "gridName": "updated_grid"
            }
            
            response = client.post("/display-config/grid-metadata/edit", json=update_data, headers=auth_headers)
            assert response.status_code == 404
    
    def test_update_grid_metadata_validation_error(self, client, auth_headers):
        """Test grid metadata update with validation error"""
        update_data = {
            "id": "invalid",  # Invalid ID type
            "gridName": "updated_grid"
        }
        
        response = client.post("/display-config/grid-metadata/edit", json=update_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_update_grid_metadata_unauthorized(self, client):
        """Test grid metadata update without authentication"""
        update_data = {
            "id": 1,
            "gridName": "updated_grid"
        }
        
        response = client.post("/display-config/grid-metadata/edit", json=update_data)
        assert response.status_code == 403
    
    def test_list_display_configs_success(self, client, mock_display_config_data):
        """Test successful display config listing"""
        with patch('display_config.controller.DisplayConfigController.list_display_configs') as mock_list:
            mock_list.return_value = [mock_display_config_data]
            
            request_data = {
                "gridNameId": "test_grid_001"
            }
            
            response = client.post("/display-config/result-display-config/list", json=request_data)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["gridNameId"] == "test_grid_001"
    
    def test_list_display_configs_validation_error(self, client):
        """Test display config listing with validation error"""
        request_data = {
            "gridNameId": 123  # Invalid type
        }
        
        response = client.post("/display-config/result-display-config/list", json=request_data)
        assert response.status_code == 400
    
    def test_update_display_configs_success(self, client, auth_headers):
        """Test successful display config update"""
        with patch('display_config.controller.DisplayConfigController.update_display_configs') as mock_update:
            mock_update.return_value = True
            
            update_data = {
                "gridNameId": "test_grid_001",
                "configs": [
                    {
                        "displayId": "test_display",
                        "title": "Test Display",
                        "hidden": False,
                        "width": 100,
                        "sortIndex": 1
                    }
                ]
            }
            
            response = client.post("/display-config/result-display-config/update", json=update_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["success"] == True
    
    def test_update_display_configs_failure(self, client, auth_headers):
        """Test display config update failure"""
        with patch('display_config.controller.DisplayConfigController.update_display_configs') as mock_update:
            mock_update.return_value = False
            
            update_data = {
                "gridNameId": "invalid_grid",
                "configs": []
            }
            
            response = client.post("/display-config/result-display-config/update", json=update_data, headers=auth_headers)
            assert response.status_code == 400
    
    def test_update_display_configs_validation_error(self, client, auth_headers):
        """Test display config update with validation error"""
        update_data = {
            "gridNameId": 123,  # Invalid type
            "configs": "invalid"  # Invalid type
        }
        
        response = client.post("/display-config/result-display-config/update", json=update_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_update_display_configs_unauthorized(self, client):
        """Test display config update without authentication"""
        update_data = {
            "gridNameId": "test_grid_001",
            "configs": []
        }
        
        response = client.post("/display-config/result-display-config/update", json=update_data)
        assert response.status_code == 403
    
    def test_create_grid_metadata_controller_exception(self, client, auth_headers):
        """Test grid metadata creation with controller exception"""
        with patch('display_config.controller.DisplayConfigController.create_grid_metadata') as mock_create:
            mock_create.side_effect = Exception("Database error")
            
            grid_data = {
                "gridName": "test_grid",
                "gridNameId": "test_grid_001"
            }
            
            response = client.post("/display-config/grid-metadata/create", json=grid_data, headers=auth_headers)
            assert response.status_code == 500
    
    def test_list_grid_metadata_controller_exception(self, client):
        """Test grid metadata listing with controller exception"""
        with patch('display_config.controller.DisplayConfigController.list_grid_metadata') as mock_list:
            mock_list.side_effect = Exception("Database error")
            
            request_data = {
                "name": "test",
                "is_active": True
            }
            
            response = client.post("/display-config/grid-metadata/list", json=request_data)
            assert response.status_code == 500
    
    def test_update_display_configs_controller_exception(self, client, auth_headers):
        """Test display config update with controller exception"""
        with patch('display_config.controller.DisplayConfigController.update_display_configs') as mock_update:
            mock_update.side_effect = Exception("Database error")
            
            update_data = {
                "gridNameId": "test_grid_001",
                "configs": []
            }
            
            response = client.post("/display-config/result-display-config/update", json=update_data, headers=auth_headers)
            assert response.status_code == 500
