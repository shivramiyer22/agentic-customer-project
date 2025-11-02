"""
Tests for main FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "chromadb" in data


def test_collections_endpoint():
    """Test collections endpoint"""
    response = client.get("/collections/")
    assert response.status_code == 200
    data = response.json()
    assert "collections" in data
    assert isinstance(data["collections"], list)

