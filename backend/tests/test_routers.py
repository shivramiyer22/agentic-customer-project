"""
Tests for API routers
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check router"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "chromadb" in data


def test_get_collections():
    """Test collections router"""
    response = client.get("/collections/")
    assert response.status_code == 200
    data = response.json()
    assert "collections" in data
    assert isinstance(data["collections"], list)
    # Should include the three main collections
    collections = data["collections"]
    assert any("billing" in col.lower() for col in collections)
    assert any("technical" in col.lower() for col in collections)
    assert any("policy" in col.lower() for col in collections)

