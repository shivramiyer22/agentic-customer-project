"""
Comprehensive tests for ingestion pipeline
"""

import pytest
import tempfile
import os
from pathlib import Path
from app.ingestion.ingest_data import (
    validate_file,
    categorize_document,
    enrich_metadata,
)
from langchain_core.documents import Document
from datetime import datetime


def create_temp_file(content: str, suffix: str = ".txt") -> Path:
    """Helper to create temporary file"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)


def test_validate_file_valid():
    """Test validate_file with valid file"""
    file_path = create_temp_file("Valid content", ".txt")
    try:
        is_valid, error = validate_file(file_path)
        assert is_valid is True
        assert error is None
    finally:
        os.unlink(file_path)


def test_validate_file_missing():
    """Test validate_file with missing file"""
    file_path = Path("/nonexistent/file.txt")
    is_valid, error = validate_file(file_path)
    assert is_valid is False
    assert error is not None
    assert "does not exist" in error.lower()


def test_validate_file_empty():
    """Test validate_file with empty file"""
    file_path = create_temp_file("", ".txt")
    try:
        is_valid, error = validate_file(file_path)
        assert is_valid is False
        assert "empty" in error.lower()
    finally:
        os.unlink(file_path)


def test_validate_file_unsupported_format():
    """Test validate_file with unsupported format"""
    file_path = create_temp_file("content", ".xyz")
    try:
        is_valid, error = validate_file(file_path)
        assert is_valid is False
        assert "unsupported" in error.lower()
    finally:
        os.unlink(file_path)


def test_validate_file_large_size():
    """Test validate_file with file exceeding size limit"""
    # Create a file and then modify its size check via mocking
    import unittest.mock as mock
    from pathlib import Path
    
    file_path = create_temp_file("A" * 1000, ".txt")
    try:
        # Mock Path.stat() to return a large size
        # Need to patch Path.stat since validate_file creates a new Path instance
        mock_stat = mock.Mock()
        mock_stat.st_size = 25 * 1024 * 1024  # 25 MB (exceeds 20 MB limit)
        
        with mock.patch('pathlib.Path.stat', return_value=mock_stat):
            is_valid, error = validate_file(file_path)
            assert is_valid is False
            assert error is not None
            assert "size" in error.lower() or "exceeds" in error.lower()
    finally:
        if file_path.exists():
            os.unlink(file_path)


def test_categorize_document_billing():
    """Test categorize_document for billing"""
    content = "This is an invoice with billing information and pricing details."
    category = categorize_document(content)
    assert "billing" in category.lower()


def test_categorize_document_technical():
    """Test categorize_document for technical"""
    content = "Technical specification manual with engineering components and bug reports."
    category = categorize_document(content)
    assert "technical" in category.lower()


def test_categorize_document_policy():
    """Test categorize_document for policy"""
    content = "FAA regulations and EASA compliance policy with DFARs requirements."
    category = categorize_document(content)
    assert "policy" in category.lower()


def test_categorize_document_filename():
    """Test categorize_document considers filename"""
    content = "Generic content"
    filename = "billing_invoice_2024.pdf"
    category = categorize_document(content, filename)
    assert "billing" in category.lower()


def test_enrich_metadata():
    """Test enrich_metadata"""
    documents = [
        Document(page_content="Content 1", metadata={"source": "test.txt"}),
        Document(page_content="Content 2", metadata={"source": "test.txt"}),
    ]
    
    source_file = Path("test.txt")
    category = "billing_knowledge_base"
    timestamp = datetime.utcnow()
    
    enriched = enrich_metadata(documents, source_file, category, timestamp)
    
    assert len(enriched) == len(documents)
    for i, doc in enumerate(enriched):
        assert "source_file" in doc.metadata
        assert "upload_timestamp" in doc.metadata
        assert "document_category" in doc.metadata
        assert "chunk_index" in doc.metadata
        assert "total_chunks" in doc.metadata
        assert doc.metadata["chunk_index"] == i
        assert doc.metadata["total_chunks"] == len(documents)
        assert doc.metadata["document_category"] == category


def test_enrich_metadata_preserves_existing():
    """Test enrich_metadata preserves existing metadata"""
    documents = [
        Document(
            page_content="Content",
            metadata={"source": "test.txt", "author": "Test Author"}
        ),
    ]
    
    enriched = enrich_metadata(
        documents,
        Path("test.txt"),
        "billing_knowledge_base"
    )
    
    assert enriched[0].metadata["source"] == "test.txt"
    assert enriched[0].metadata["author"] == "Test Author"


def test_enrich_metadata_default_timestamp():
    """Test enrich_metadata uses current timestamp if not provided"""
    documents = [Document(page_content="Content", metadata={})]
    
    enriched = enrich_metadata(
        documents,
        Path("test.txt"),
        "technical_knowledge_base"
    )
    
    assert "upload_timestamp" in enriched[0].metadata
    assert enriched[0].metadata["upload_timestamp"] is not None

