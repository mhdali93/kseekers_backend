"""
Unit tests for health check routes
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

class TestHealthRoutes:
    """Test cases for health check routes"""
    
    def test_health_check_success(self, client):
        """Test successful health check"""
        response = client.get("/healthCheck")
        assert response.status_code == 200
        assert response.text == '"202"'
    
    def test_health_check_response_format(self, client):
        """Test health check response format"""
        response = client.get("/healthCheck")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert response.text in ['"202"', '202']
    
    def test_health_check_endpoint_exists(self, client):
        """Test that health check endpoint exists and is accessible"""
        response = client.get("/healthCheck")
        assert response.status_code == 200
        assert "healthCheck" in str(response.url)
