"""
Tests for health router
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint_success():
    """Test health endpoint returns success"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "chromadb" in data
    assert "timestamp" in data
    
    chromadb = data["chromadb"]
    assert "connected" in chromadb
    assert "collections_count" in chromadb


def test_health_endpoint_structure():
    """Test health endpoint response structure"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert isinstance(data["status"], str)
    assert isinstance(data["chromadb"], dict)
    assert isinstance(data["timestamp"], str)
    
    chromadb = data["chromadb"]
    assert isinstance(chromadb["connected"], bool)
    assert isinstance(chromadb["collections_count"], int)


def test_health_endpoint_chromadb_connection():
    """Test health endpoint verifies ChromaDB connection"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    
    # ChromaDB should be connected in test environment
    chromadb = data["chromadb"]
    assert chromadb["connected"] is True

