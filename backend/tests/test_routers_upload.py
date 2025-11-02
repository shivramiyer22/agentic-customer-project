"""
Tests for upload router
"""

import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_test_file(content: str, suffix: str = ".txt") -> Path:
    """Helper to create temporary test file"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)


@pytest.fixture
def sample_txt_file():
    """Fixture for sample text file"""
    file_path = create_test_file("Sample text content for testing")
    yield file_path
    if file_path.exists():
        os.unlink(file_path)


@pytest.fixture
def sample_json_file():
    """Fixture for sample JSON file"""
    content = '{"key": "value", "number": 123}'
    file_path = create_test_file(content, ".json")
    yield file_path
    if file_path.exists():
        os.unlink(file_path)


def test_upload_endpoint_no_files():
    """Test upload endpoint with no files"""
    response = client.post("/upload/")
    assert response.status_code == 422  # Validation error


def test_upload_endpoint_invalid_file():
    """Test upload endpoint with invalid file"""
    # Create a file with unsupported extension
    invalid_file = create_test_file("test content", ".xyz")
    try:
        files = [("files", (invalid_file.name, open(invalid_file, "rb"), "application/octet-stream"))]
        response = client.post("/upload/", files=files, data={"target_collection": "auto-map"})
        # Should either validate or accept and mark as failed
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.json()
            assert "upload_id" in data
    finally:
        os.unlink(invalid_file)


def test_upload_endpoint_valid_file(sample_txt_file):
    """Test upload endpoint with valid file"""
    with open(sample_txt_file, "rb") as f:
        files = [("files", (sample_txt_file.name, f, "text/plain"))]
        response = client.post(
            "/upload/",
            files=files,
            data={"target_collection": "auto-map"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "upload_id" in data
        assert "status" in data
        assert "files" in data
        assert isinstance(data["files"], list)
        assert len(data["files"]) > 0
        assert "overall_progress" in data
        assert "created_at" in data


def test_upload_endpoint_multiple_files(sample_txt_file, sample_json_file):
    """Test upload endpoint with multiple files"""
    with open(sample_txt_file, "rb") as f1, open(sample_json_file, "rb") as f2:
        files = [
            ("files", (sample_txt_file.name, f1, "text/plain")),
            ("files", (sample_json_file.name, f2, "application/json"))
        ]
        response = client.post(
            "/upload/",
            files=files,
            data={"target_collection": "auto-map"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "upload_id" in data
        assert len(data["files"]) == 2


def test_upload_endpoint_target_collection():
    """Test upload endpoint with specific target collection"""
    sample_file = create_test_file("test content")
    try:
        with open(sample_file, "rb") as f:
            files = [("files", (sample_file.name, f, "text/plain"))]
            response = client.post(
                "/upload/",
                files=files,
                data={"target_collection": "billing_knowledge_base"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "upload_id" in data
    finally:
        os.unlink(sample_file)


def test_get_upload_status(sample_txt_file):
    """Test GET /upload/status/{upload_id} endpoint"""
    # First upload a file
    with open(sample_txt_file, "rb") as f:
        files = [("files", (sample_txt_file.name, f, "text/plain"))]
        upload_response = client.post(
            "/upload/",
            files=files,
            data={"target_collection": "auto-map"}
        )
        
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        upload_id = upload_data["upload_id"]
        
        # Get status
        status_response = client.get(f"/upload/status/{upload_id}")
        assert status_response.status_code == 200
        
        status_data = status_response.json()
        assert "upload_id" in status_data
        assert "status" in status_data
        assert "files" in status_data
        assert "overall_progress" in status_data
        assert "created_at" in status_data
        assert "updated_at" in status_data


def test_get_upload_status_not_found():
    """Test GET /upload/status/{upload_id} with non-existent ID"""
    response = client.get("/upload/status/non-existent-id")
    assert response.status_code == 404


def test_upload_endpoint_file_validation():
    """Test upload endpoint file validation"""
    # Test with empty file (should fail validation)
    empty_file = create_test_file("", ".txt")
    try:
        with open(empty_file, "rb") as f:
            files = [("files", (empty_file.name, f, "text/plain"))]
            response = client.post(
                "/upload/",
                files=files,
                data={"target_collection": "auto-map"}
            )
            
            # Empty file should return 400 (Bad Request) because validation fails before upload
            # OR return 200 with file marked as failed - both are acceptable
            assert response.status_code in [200, 400]
            
            if response.status_code == 200:
                # If 200, file should be marked as failed
                data = response.json()
                assert len(data["files"]) > 0
                file_status = data["files"][0]
                assert file_status["status"] == "failed"
                assert file_status["error"] is not None
            else:
                # If 400, check error message
                data = response.json()
                assert "detail" in data
    finally:
        if empty_file.exists():
            os.unlink(empty_file)

