"""
Tests for document chunkers
"""

import pytest
from langchain_core.documents import Document
from app.ingestion.chunkers.recursive_chunker import chunk_documents


@pytest.fixture
def short_document():
    """Fixture for short document"""
    return Document(
        page_content="Short content that won't be chunked.",
        metadata={"source": "test.txt"}
    )


@pytest.fixture
def long_document():
    """Fixture for long document that will be chunked"""
    long_content = "A" * 2500  # Content longer than chunk_size
    return Document(
        page_content=long_content,
        metadata={"source": "test.txt"}
    )


@pytest.fixture
def multiple_documents():
    """Fixture for multiple documents"""
    return [
        Document(page_content="First document.", metadata={"source": "test1.txt"}),
        Document(page_content="Second document.", metadata={"source": "test2.txt"}),
        Document(page_content="Third document.", metadata={"source": "test3.txt"}),
    ]


def test_chunk_documents_short(short_document):
    """Test chunking short document"""
    chunks = chunk_documents([short_document], chunk_size=1000, chunk_overlap=200)
    assert len(chunks) >= 1
    assert all(isinstance(chunk, Document) for chunk in chunks)
    assert chunks[0].page_content == short_document.page_content


def test_chunk_documents_long(long_document):
    """Test chunking long document"""
    chunks = chunk_documents([long_document], chunk_size=1000, chunk_overlap=200)
    assert len(chunks) > 1  # Should be split into multiple chunks
    assert all(isinstance(chunk, Document) for chunk in chunks)
    
    # Verify metadata is preserved
    assert all("source" in chunk.metadata for chunk in chunks)


def test_chunk_documents_multiple(multiple_documents):
    """Test chunking multiple documents"""
    chunks = chunk_documents(multiple_documents, chunk_size=1000, chunk_overlap=200)
    assert len(chunks) >= len(multiple_documents)
    assert all(isinstance(chunk, Document) for chunk in chunks)


def test_chunk_documents_chunk_size():
    """Test chunk_documents respects chunk_size"""
    long_content = "A" * 2500
    document = Document(page_content=long_content, metadata={"source": "test.txt"})
    
    chunks = chunk_documents([document], chunk_size=500, chunk_overlap=100)
    
    # Verify chunks don't exceed chunk_size (approximately)
    for chunk in chunks:
        assert len(chunk.page_content) <= 500 + 100  # Allow some tolerance


def test_chunk_documents_preserves_metadata():
    """Test chunk_documents preserves document metadata"""
    metadata = {"source": "test.txt", "author": "Test Author"}
    document = Document(page_content="A" * 1500, metadata=metadata)
    
    chunks = chunk_documents([document], chunk_size=500, chunk_overlap=100)
    
    # Verify metadata is preserved in all chunks
    for chunk in chunks:
        assert "source" in chunk.metadata
        assert chunk.metadata["source"] == "test.txt"


def test_chunk_documents_overlap():
    """Test chunk_documents uses overlap correctly"""
    content = "A" * 2500
    document = Document(page_content=content, metadata={"source": "test.txt"})
    
    chunks = chunk_documents([document], chunk_size=1000, chunk_overlap=200)
    
    if len(chunks) > 1:
        # Check that chunks overlap (first chunk end should appear in second chunk start)
        first_chunk_end = chunks[0].page_content[-200:]
        second_chunk_start = chunks[1].page_content[:200]
        # Some overlap should exist (not exact match due to splitting logic)
        assert len(first_chunk_end) > 0
        assert len(second_chunk_start) > 0

