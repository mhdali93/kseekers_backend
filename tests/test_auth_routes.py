"""
Unit tests for authentication routes
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime, timedelta
import json

class TestAuthRoutes:
    """Test cases for authentication routes"""
    
    def test_register_user_success(self, client, mock_user_data):
        """Test successful user registration"""
        with patch('auth.controller.AuthController.register_user') as mock_register:
            mock_user = Mock()
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.email = "test@example.com"
            mock_user.phone = "1234567890"
            mock_user.is_admin = False
            mock_register.return_value = mock_user
            
            user_data = {
                "username": "testuser",
                "email": "test@example.com",
                "phone": "1234567890"
            }
            
            response = client.post("/auth/register", json=user_data)
            assert response.status_code == 201
            response_data = response.json()
            # Check the wrapped response format
            assert "result" in response_data
            assert response_data["result"]["payload"]["id"] == 1
            assert response_data["result"]["payload"]["username"] == "testuser"
            assert response_data["result"]["payload"]["email"] == "test@example.com"
    
    def test_register_user_validation_error(self, client):
        """Test user registration with validation error"""
        user_data = {
            "username": "",  # Invalid empty username
            "email": "invalid-email",  # Invalid email format
            "phone": "123"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400  # Bad request (actual API behavior)
    
    def test_request_otp_success(self, client, mock_user_data):
        """Test successful OTP request"""
        with patch('auth.controller.AuthController.get_user') as mock_get_user, \
             patch('auth.controller.AuthController.generate_otp') as mock_generate_otp:
            
            mock_user = Mock()
            mock_user.id = 1
            mock_user.email = "test@example.com"
            mock_get_user.return_value = mock_user
            mock_generate_otp.return_value = None
            
            otp_data = {
                "username_or_email": "test@example.com"
            }
            
            response = client.post("/auth/otp/request", json=otp_data)
            assert response.status_code == 200
            response_data = response.json()
            # Check the wrapped response format
            assert "result" in response_data
            assert response_data["result"]["payload"]["email"] == "test@example.com"
    
    def test_request_otp_user_not_found(self, client):
        """Test OTP request with user not found"""
        with patch('auth.controller.AuthController.get_user') as mock_get_user:
            mock_get_user.return_value = None
            
            otp_data = {
                "username_or_email": "nonexistent@example.com"
            }
            
            response = client.post("/auth/otp/request", json=otp_data)
            assert response.status_code == 404
    
    def test_verify_otp_success(self, client, mock_jwt_token):
        """Test successful OTP verification"""
        with patch('auth.controller.AuthController.login') as mock_login:
            mock_login.return_value = mock_jwt_token
            
            verify_data = {
                "username_or_email": "test@example.com",
                "otp_code": "123456"
            }
            
            response = client.post("/auth/otp/verify", json=verify_data)
            assert response.status_code == 200
            response_data = response.json()
            # Check the wrapped response format
            assert "result" in response_data
            assert "access_token" in response_data["result"]["payload"]
            assert response_data["result"]["payload"]["token_type"] == "bearer"
    
    def test_verify_otp_invalid_code(self, client):
        """Test OTP verification with invalid code"""
        with patch('auth.controller.AuthController.login') as mock_login:
            from fastapi import HTTPException
            mock_login.side_effect = HTTPException(status_code=400, detail="Invalid OTP")
            
            verify_data = {
                "username_or_email": "test@example.com",
                "otp_code": "invalid"
            }
            
            response = client.post("/auth/otp/verify", json=verify_data)
            assert response.status_code == 400
    
    def test_get_current_user_success(self, client, mock_user_data, auth_headers):
        """Test successful get current user"""
        with patch('auth.controller.AuthController.get_user_by_id') as mock_get_user:
            mock_user = Mock()
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_user.email = "test@example.com"
            mock_user.phone = "1234567890"
            mock_user.is_admin = False
            mock_get_user.return_value = mock_user
            
            response = client.get("/auth/me", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            # Check the wrapped response format
            assert "result" in response_data
            assert response_data["result"]["payload"]["id"] == 1
            assert response_data["result"]["payload"]["username"] == "testuser"
    
    def test_get_current_user_not_found(self, client, auth_headers):
        """Test get current user when user not found"""
        with patch('auth.controller.AuthController.get_user_by_id') as mock_get_user:
            mock_get_user.return_value = None
            
            response = client.get("/auth/me", headers=auth_headers)
            assert response.status_code == 404
    
    def test_get_current_user_unauthorized(self, client):
        """Test get current user without authentication"""
        response = client.get("/auth/me")
        assert response.status_code == 403  # Forbidden (actual API behavior)
    
    def test_refresh_token_success(self, client, mock_jwt_token):
        """Test successful token refresh"""
        with patch('auth.controller.AuthController.refresh_token') as mock_refresh:
            new_token = "new_refreshed_token"
            mock_refresh.return_value = new_token
            
            refresh_data = {
                "access_token": mock_jwt_token
            }
            
            response = client.post("/auth/refresh", json=refresh_data)
            assert response.status_code == 200
            response_data = response.json()
            # Check the wrapped response format
            assert "result" in response_data
            assert response_data["result"]["payload"]["access_token"] == new_token
            assert response_data["result"]["payload"]["token_type"] == "bearer"
    
    def test_refresh_token_invalid(self, client):
        """Test token refresh with invalid token"""
        with patch('auth.controller.AuthController.refresh_token') as mock_refresh:
            from fastapi import HTTPException
            mock_refresh.side_effect = HTTPException(status_code=401, detail="Invalid token")
            
            refresh_data = {
                "access_token": "invalid_token"
            }
            
            response = client.post("/auth/refresh", json=refresh_data)
            assert response.status_code == 401
    
    def test_register_user_controller_exception(self, client):
        """Test user registration with controller exception"""
        with patch('auth.controller.AuthController.register_user') as mock_register:
            mock_register.side_effect = Exception("Database error")
            
            user_data = {
                "username": "testuser",
                "email": "test@example.com",
                "phone": "1234567890"
            }
            
            response = client.post("/auth/register", json=user_data)
            assert response.status_code == 500
    
    def test_request_otp_controller_exception(self, client):
        """Test OTP request with controller exception"""
        with patch('auth.controller.AuthController.get_user') as mock_get_user:
            mock_get_user.side_effect = Exception("Database error")
            
            otp_data = {
                "username_or_email": "test@example.com"
            }
            
            response = client.post("/auth/otp/request", json=otp_data)
            assert response.status_code == 500
    
    def test_verify_otp_controller_exception(self, client):
        """Test OTP verification with controller exception"""
        with patch('auth.controller.AuthController.login') as mock_login:
            mock_login.side_effect = Exception("Database error")
            
            verify_data = {
                "username_or_email": "test@example.com",
                "otp_code": "123456"
            }
            
            response = client.post("/auth/otp/verify", json=verify_data)
            assert response.status_code == 500
