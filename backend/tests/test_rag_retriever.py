"""
Tests for RAG (Retrieval-Augmented Generation) retrieval implementation

Tests for Pure RAG retrieval strategy for technical documents
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.documents import Document
from app.retrieval.rag_retriever import search_technical_kb, format_technical_context
from app.utils.config import config


def test_search_technical_kb_tool_decorated():
    """Test that search_technical_kb is decorated as a tool"""
    # The @tool decorator wraps the function in a StructuredTool
    # Check if it has tool attributes
    assert hasattr(search_technical_kb, 'description') or hasattr(search_technical_kb, 'name')
    # Check if it can be invoked (tool has invoke method)
    assert hasattr(search_technical_kb, 'invoke') or hasattr(search_technical_kb, '__call__')


def test_search_technical_kb_no_documents():
    """Test search_technical_kb when no documents are found"""
    with patch('app.retrieval.rag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        result = search_technical_kb.invoke({"query": "test technical"})
        
        assert result is not None
        assert "No relevant technical documents" in result or "not found" in result.lower()


def test_search_technical_kb_with_documents():
    """Test search_technical_kb when documents are found"""
    with patch('app.retrieval.rag_retriever.get_chroma_client') as mock_get_client:
        # Create mock documents
        mock_doc1 = Document(
            page_content="API endpoint /users requires authentication token...",
            metadata={"source_file": "api_docs.md", "document_category": "technical"}
        )
        mock_doc2 = Document(
            page_content="Component specification for engine requires...",
            metadata={"source_file": "engine_specs.pdf", "document_category": "technical"}
        )
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = [mock_doc1, mock_doc2]
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        result = search_technical_kb.invoke({"query": "API documentation"})
        
        assert result is not None
        assert "API endpoint" in result or "authentication" in result
        assert "api_docs.md" in result or "Source" in result


def test_search_technical_kb_uses_technical_collection():
    """Test that search_technical_kb uses the correct collection"""
    with patch('app.retrieval.rag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_technical_kb.invoke({"query": "test"})
        
        # Verify it was called with technical collection name
        mock_client.get_or_create_collection.assert_called_once()
        call_args = mock_client.get_or_create_collection.call_args
        assert call_args[1]['collection_name'] == config.COLLECTION_TECHNICAL


def test_search_technical_kb_error_handling():
    """Test that search_technical_kb handles errors gracefully"""
    with patch('app.retrieval.rag_retriever.get_chroma_client') as mock_get_client:
        mock_get_client.side_effect = Exception("Database error")
        
        result = search_technical_kb.invoke({"query": "test"})
        
        assert result is not None
        assert "Error" in result or "error" in result.lower()


def test_format_technical_context():
    """Test format_technical_context formatting"""
    docs = [
        Document(
            page_content="Technical content 1",
            metadata={
                "source_file": "tech1.pdf",
                "document_category": "technical",
                "chunk_index": 0,
                "upload_timestamp": "2024-01-01"
            }
        ),
        Document(
            page_content="Technical content 2",
            metadata={
                "source_file": "tech2.pdf",
                "document_category": "technical",
                "chunk_index": 1
            }
        ),
    ]
    
    result = format_technical_context(docs, "test query")
    
    assert result is not None
    assert "test query" in result
    assert "Technical content 1" in result
    assert "Technical content 2" in result
    assert "tech1.pdf" in result or "Source" in result
    assert "tech2.pdf" in result or "Source" in result


def test_format_technical_context_empty_docs():
    """Test format_technical_context with empty documents list"""
    result = format_technical_context([], "test query")
    
    assert result is not None
    assert "test query" in result


def test_format_technical_context_source_citations():
    """Test that format_technical_context includes source citations"""
    docs = [
        Document(
            page_content="Test technical content",
            metadata={"source_file": "test_tech.pdf", "document_category": "technical"}
        )
    ]
    
    result = format_technical_context(docs, "test query")
    
    assert "Source" in result
    assert "test_tech.pdf" in result


def test_search_technical_kb_default_k():
    """Test that search_technical_kb uses default k=3"""
    with patch('app.retrieval.rag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_technical_kb.invoke({"query": "test"})
        
        # Verify similarity_search was called with k=3
        mock_collection.similarity_search.assert_called_once()
        call_kwargs = mock_collection.similarity_search.call_args[1]
        assert call_kwargs.get('k', 3) == 3


def test_search_technical_kb_custom_k():
    """Test that search_technical_kb accepts custom k parameter"""
    with patch('app.retrieval.rag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_technical_kb.invoke({"query": "test", "k": 5})
        
        # Verify similarity_search was called with custom k
        call_kwargs = mock_collection.similarity_search.call_args[1]
        assert call_kwargs.get('k') == 5





