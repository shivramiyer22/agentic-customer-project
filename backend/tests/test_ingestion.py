"""
Tests for document ingestion pipeline
"""

import pytest
import tempfile
import os
from pathlib import Path
from app.ingestion.parsers.parser_factory import parse_document, get_parser
from app.ingestion.chunkers.recursive_chunker import chunk_documents
from app.ingestion.ingest_data import validate_file, categorize_document
from langchain_core.documents import Document


def test_get_parser():
    """Test parser factory"""
    # Test PDF parser
    parser = get_parser("test.pdf")
    assert parser is not None
    
    # Test TXT parser
    parser = get_parser("test.txt")
    assert parser is not None
    
    # Test unsupported extension
    with pytest.raises(ValueError):
        get_parser("test.xyz")


def test_validate_file():
    """Test file validation"""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    
    try:
        is_valid, error = validate_file(temp_path)
        assert is_valid
        assert error is None
    finally:
        os.unlink(temp_path)


def test_validate_file_invalid_extension():
    """Test file validation with invalid extension"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    
    try:
        is_valid, error = validate_file(temp_path)
        assert not is_valid
        assert error is not None
    finally:
        os.unlink(temp_path)


def test_categorize_document_billing():
    """Test document categorization for billing"""
    content = "This is an invoice with pricing information and billing details."
    category = categorize_document(content)
    assert "billing" in category.lower()


def test_categorize_document_technical():
    """Test document categorization for technical"""
    content = "Technical specification manual with bug reports and engineering components."
    category = categorize_document(content)
    assert "technical" in category.lower()


def test_categorize_document_policy():
    """Test document categorization for policy"""
    content = "FAA regulations and EASA compliance policy with DFARs requirements."
    category = categorize_document(content)
    assert "policy" in category.lower()


def test_chunk_documents():
    """Test document chunking"""
    # Create test documents
    documents = [
        Document(page_content="Short content", metadata={"source": "test1.txt"}),
        Document(
            page_content="A" * 2000,  # Long content that will be chunked
            metadata={"source": "test2.txt"}
        ),
    ]
    
    chunks = chunk_documents(documents, chunk_size=1000, chunk_overlap=200)
    assert len(chunks) >= len(documents)  # Should have at least as many chunks as documents
    assert all(isinstance(chunk, Document) for chunk in chunks)

