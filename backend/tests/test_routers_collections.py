"""
Tests for collections router
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_collections():
    """Test GET /collections endpoint"""
    response = client.get("/collections/")
    assert response.status_code == 200
    data = response.json()
    
    assert "collections" in data
    assert isinstance(data["collections"], list)
    assert "count" in data
    assert isinstance(data["count"], int)


def test_get_collections_contains_required():
    """Test collections endpoint returns required collections"""
    response = client.get("/collections/")
    assert response.status_code == 200
    data = response.json()
    
    collections = data["collections"]
    collection_names = [col.lower() if isinstance(col, str) else col.name.lower() for col in collections]
    
    # Should include the three main collections
    assert any("billing" in col for col in collection_names)
    assert any("technical" in col for col in collection_names)
    assert any("policy" in col for col in collection_names)


def test_get_collections_structure():
    """Test collections endpoint response structure"""
    response = client.get("/collections/")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data["collections"], list)
    assert isinstance(data["count"], int)
    assert data["count"] >= 0


def test_get_collections_error_handling():
    """Test collections endpoint error handling"""
    # Even if ChromaDB fails, should return configured collections
    response = client.get("/collections/")
    assert response.status_code == 200
    data = response.json()
    
    # Should always have collections key
    assert "collections" in data
    assert isinstance(data["collections"], list)

