"""
Integration tests for the backend application
"""

import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_temp_file(content: str, suffix: str = ".txt") -> Path:
    """Helper to create temporary file"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)


def test_health_then_collections():
    """Test health check then collections listing"""
    # First check health
    health_response = client.get("/health/")
    assert health_response.status_code == 200
    
    # Then get collections
    collections_response = client.get("/collections/")
    assert collections_response.status_code == 200
    
    # Verify collections response
    collections_data = collections_response.json()
    assert "collections" in collections_data
    assert len(collections_data["collections"]) > 0


def test_upload_then_status():
    """Test upload then status check flow"""
    # Create test file
    sample_file = create_temp_file("Test content for integration testing")
    
    try:
        # Upload file
        with open(sample_file, "rb") as f:
            files = [("files", (sample_file.name, f, "text/plain"))]
            upload_response = client.post(
                "/upload/",
                files=files,
                data={"target_collection": "auto-map"}
            )
            
            assert upload_response.status_code == 200
            upload_data = upload_response.json()
            upload_id = upload_data["upload_id"]
            
            # Check status
            status_response = client.get(f"/upload/status/{upload_id}")
            assert status_response.status_code == 200
            
            status_data = status_response.json()
            assert status_data["upload_id"] == upload_id
            
    finally:
        os.unlink(sample_file)


def test_collections_then_upload():
    """Test collections listing then upload to specific collection"""
    # Get collections
    collections_response = client.get("/collections/")
    assert collections_response.status_code == 200
    collections_data = collections_response.json()
    
    # Find a valid collection (not auto-map)
    valid_collections = [
        col for col in collections_data["collections"]
        if isinstance(col, str) and "knowledge_base" in col
    ]
    
    if valid_collections:
        target_collection = valid_collections[0]
        
        # Upload to specific collection
        sample_file = create_temp_file("Test content")
        try:
            with open(sample_file, "rb") as f:
                files = [("files", (sample_file.name, f, "text/plain"))]
                upload_response = client.post(
                    "/upload/",
                    files=files,
                    data={"target_collection": target_collection}
                )
                
                assert upload_response.status_code == 200
        finally:
            os.unlink(sample_file)


def test_end_to_end_upload_flow():
    """Test complete end-to-end upload flow"""
    # 1. Check health
    health = client.get("/health/").json()
    assert health["status"] == "healthy"
    
    # 2. Get collections
    collections = client.get("/collections/").json()
    assert len(collections["collections"]) > 0
    
    # 3. Upload file
    sample_file = create_temp_file(
        "This is a billing invoice with pricing information for parts catalog."
    )
    
    try:
        with open(sample_file, "rb") as f:
            files = [("files", (sample_file.name, f, "text/plain"))]
            upload_response = client.post(
                "/upload/",
                files=files,
                data={"target_collection": "auto-map"}
            )
            
            assert upload_response.status_code == 200
            upload_data = upload_response.json()
            
            # 4. Check upload status
            upload_id = upload_data["upload_id"]
            status = client.get(f"/upload/status/{upload_id}").json()
            
            assert status["upload_id"] == upload_id
            assert "status" in status
            assert "files" in status
            
    finally:
        os.unlink(sample_file)

