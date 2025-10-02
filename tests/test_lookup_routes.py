"""
Unit tests for lookup routes
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime

class TestLookupRoutes:
    """Test cases for lookup routes"""
    
    def test_get_lookup_types_success(self, client, mock_lookup_type_data):
        """Test successful lookup types retrieval"""
        with patch('look_up.controller.LookUpController.get_lookup_types') as mock_get_types:
            mock_get_types.return_value = [mock_lookup_type_data]
            
            response = client.get("/lookup/types")
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["name"] == "test_type"
    
    def test_get_lookup_types_controller_exception(self, client):
        """Test lookup types retrieval with controller exception"""
        with patch('look_up.controller.LookUpController.get_lookup_types') as mock_get_types:
            mock_get_types.side_effect = Exception("Database error")
            
            response = client.get("/lookup/types")
            assert response.status_code == 500
    
    def test_get_lookup_values_by_type_success(self, client, mock_lookup_value_data):
        """Test successful lookup values retrieval by type"""
        with patch('look_up.controller.LookUpController.get_lookup_values_by_type') as mock_get_values:
            mock_get_values.return_value = [mock_lookup_value_data]
            
            request_data = {
                "type_name": "test_type"
            }
            
            response = client.post("/lookup/values", json=request_data)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 1
            assert response_data["result"]["payload"][0]["code"] == "test_code"
    
    def test_get_lookup_values_by_type_validation_error(self, client):
        """Test lookup values retrieval with validation error"""
        request_data = {
            "type_name": 123  # Invalid type
        }
        
        response = client.post("/lookup/values", json=request_data)
        assert response.status_code == 400
    
    def test_get_lookup_values_by_type_controller_exception(self, client):
        """Test lookup values retrieval with controller exception"""
        with patch('look_up.controller.LookUpController.get_lookup_values_by_type') as mock_get_values:
            mock_get_values.side_effect = Exception("Database error")
            
            request_data = {
                "type_name": "test_type"
            }
            
            response = client.post("/lookup/values", json=request_data)
            assert response.status_code == 500
    
    def test_manage_lookup_type_success(self, client, mock_lookup_type_data, auth_headers):
        """Test successful lookup type management"""
        with patch('look_up.controller.LookUpController.manage_lookup_type') as mock_manage_type:
            mock_manage_type.return_value = mock_lookup_type_data
            
            type_data = {
                "name": "test_type",
                "description": "Test lookup type"
            }
            
            response = client.post("/lookup/types/manage", json=type_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["name"] == "test_type"
    
    def test_manage_lookup_type_validation_error(self, client, auth_headers):
        """Test lookup type management with validation error"""
        type_data = {
            "name": "",  # Invalid empty name
            "description": "Test lookup type"
        }
        
        response = client.post("/lookup/types/manage", json=type_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_manage_lookup_type_unauthorized(self, client):
        """Test lookup type management without authentication"""
        type_data = {
            "name": "test_type",
            "description": "Test lookup type"
        }
        
        response = client.post("/lookup/types/manage", json=type_data)
        assert response.status_code == 403
    
    def test_manage_lookup_type_controller_exception(self, client, auth_headers):
        """Test lookup type management with controller exception"""
        with patch('look_up.controller.LookUpController.manage_lookup_type') as mock_manage_type:
            mock_manage_type.side_effect = Exception("Database error")
            
            type_data = {
                "name": "test_type",
                "description": "Test lookup type"
            }
            
            response = client.post("/lookup/types/manage", json=type_data, headers=auth_headers)
            assert response.status_code == 500
    
    def test_manage_lookup_values_success(self, client, auth_headers):
        """Test successful lookup values management"""
        with patch('look_up.controller.LookUpController.manage_lookup_values') as mock_manage_values:
            mock_manage_values.return_value = True
            
            request_data = {
                "type_name": "test_type",
                "values": [
                    {
                        "code": "test_code",
                        "value": "Test Value",
                        "description": "Test lookup value",
                        "is_active": True,
                        "sort_order": 1
                    }
                ]
            }
            
            response = client.post("/lookup/values/manage", json=request_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["type_name"] == "test_type"
            assert response_data["result"]["payload"]["success"] == True
    
    def test_manage_lookup_values_failure(self, client, auth_headers):
        """Test lookup values management failure"""
        with patch('look_up.controller.LookUpController.manage_lookup_values') as mock_manage_values:
            mock_manage_values.return_value = False
            
            request_data = {
                "type_name": "invalid_type",
                "values": []
            }
            
            response = client.post("/lookup/values/manage", json=request_data, headers=auth_headers)
            assert response.status_code == 400
    
    def test_manage_lookup_values_validation_error(self, client, auth_headers):
        """Test lookup values management with validation error"""
        request_data = {
            "type_name": 123,  # Invalid type
            "values": "invalid"  # Invalid type
        }
        
        response = client.post("/lookup/values/manage", json=request_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_manage_lookup_values_unauthorized(self, client):
        """Test lookup values management without authentication"""
        request_data = {
            "type_name": "test_type",
            "values": []
        }
        
        response = client.post("/lookup/values/manage", json=request_data)
        assert response.status_code == 403
    
    def test_manage_lookup_values_controller_exception(self, client, auth_headers):
        """Test lookup values management with controller exception"""
        with patch('look_up.controller.LookUpController.manage_lookup_values') as mock_manage_values:
            mock_manage_values.side_effect = Exception("Database error")
            
            request_data = {
                "type_name": "test_type",
                "values": []
            }
            
            response = client.post("/lookup/values/manage", json=request_data, headers=auth_headers)
            assert response.status_code == 500
    
    def test_get_lookup_types_empty_result(self, client):
        """Test lookup types retrieval with empty result"""
        with patch('look_up.controller.LookUpController.get_lookup_types') as mock_get_types:
            mock_get_types.return_value = []
            
            response = client.get("/lookup/types")
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 0
    
    def test_get_lookup_values_by_type_empty_result(self, client):
        """Test lookup values retrieval with empty result"""
        with patch('look_up.controller.LookUpController.get_lookup_values_by_type') as mock_get_values:
            mock_get_values.return_value = []
            
            request_data = {
                "type_name": "nonexistent_type"
            }
            
            response = client.post("/lookup/values", json=request_data)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data["result"]["payload"]) == 0
    
    def test_manage_lookup_type_with_none_values(self, client, auth_headers):
        """Test lookup type management with None values"""
        with patch('look_up.controller.LookUpController.manage_lookup_type') as mock_manage_type:
            mock_manage_type.return_value = {"name": "test_type"}
            
            type_data = {
                "name": "test_type",
                "description": None  # None value
            }
            
            response = client.post("/lookup/types/manage", json=type_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["name"] == "test_type"
    
    def test_manage_lookup_values_with_empty_list(self, client, auth_headers):
        """Test lookup values management with empty values list"""
        with patch('look_up.controller.LookUpController.manage_lookup_values') as mock_manage_values:
            mock_manage_values.return_value = True
            
            request_data = {
                "type_name": "test_type",
                "values": []  # Empty list
            }
            
            response = client.post("/lookup/values/manage", json=request_data, headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["result"]["payload"]["success"] == True
