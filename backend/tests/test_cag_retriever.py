"""
Tests for CAG (Cached Augmented Generation) retrieval implementation

Tests for Pure CAG retrieval strategy for policy documents
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.documents import Document
from app.retrieval.cag_retriever import search_policy_kb, format_policy_context
from app.utils.config import config


def test_search_policy_kb_tool_decorated():
    """Test that search_policy_kb is decorated as a tool"""
    # The @tool decorator wraps the function in a StructuredTool
    # Check if it has tool attributes
    assert hasattr(search_policy_kb, 'description') or hasattr(search_policy_kb, 'name')
    # Check if it can be invoked (tool has invoke method)
    assert hasattr(search_policy_kb, 'invoke') or hasattr(search_policy_kb, '__call__')


def test_search_policy_kb_no_documents():
    """Test search_policy_kb when no documents are found"""
    with patch('app.retrieval.cag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        result = search_policy_kb.invoke({"query": "test policy"})
        
        assert result is not None
        assert "No relevant policy documents" in result or "not found" in result.lower()


def test_search_policy_kb_with_documents():
    """Test search_policy_kb when documents are found"""
    with patch('app.retrieval.cag_retriever.get_chroma_client') as mock_get_client:
        # Create mock documents
        mock_doc1 = Document(
            page_content="FAA regulation 14 CFR Part 121 requires...",
            metadata={"source_file": "faa_regulations.pdf", "document_category": "policy"}
        )
        mock_doc2 = Document(
            page_content="EASA regulation requires compliance with...",
            metadata={"source_file": "easa_policies.pdf", "document_category": "policy"}
        )
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = [mock_doc1, mock_doc2]
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        result = search_policy_kb.invoke({"query": "FAA regulations"})
        
        assert result is not None
        assert "FAA regulation" in result or "14 CFR" in result
        assert "faa_regulations.pdf" in result or "Source" in result


def test_search_policy_kb_uses_policy_collection():
    """Test that search_policy_kb uses the correct collection"""
    with patch('app.retrieval.cag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_policy_kb.invoke({"query": "test"})
        
        # Verify it was called with policy collection name
        mock_client.get_or_create_collection.assert_called_once()
        call_args = mock_client.get_or_create_collection.call_args
        assert call_args[1]['collection_name'] == config.COLLECTION_POLICY


def test_search_policy_kb_error_handling():
    """Test that search_policy_kb handles errors gracefully"""
    with patch('app.retrieval.cag_retriever.get_chroma_client') as mock_get_client:
        mock_get_client.side_effect = Exception("Database error")
        
        result = search_policy_kb.invoke({"query": "test"})
        
        assert result is not None
        assert "Error" in result or "error" in result.lower()


def test_format_policy_context():
    """Test format_policy_context formatting"""
    docs = [
        Document(
            page_content="Policy content 1",
            metadata={
                "source_file": "policy1.pdf",
                "document_category": "policy",
                "chunk_index": 0,
                "upload_timestamp": "2024-01-01"
            }
        ),
        Document(
            page_content="Policy content 2",
            metadata={
                "source_file": "policy2.pdf",
                "document_category": "policy",
                "chunk_index": 1
            }
        ),
    ]
    
    result = format_policy_context(docs, "test query")
    
    assert result is not None
    assert "test query" in result
    assert "Policy content 1" in result
    assert "Policy content 2" in result
    assert "policy1.pdf" in result or "Source" in result
    assert "policy2.pdf" in result or "Source" in result


def test_format_policy_context_empty_docs():
    """Test format_policy_context with empty documents list"""
    result = format_policy_context([], "test query")
    
    assert result is not None
    assert "test query" in result


def test_format_policy_context_source_citations():
    """Test that format_policy_context includes source citations"""
    docs = [
        Document(
            page_content="Test policy content",
            metadata={"source_file": "test_policy.pdf", "document_category": "policy"}
        )
    ]
    
    result = format_policy_context(docs, "test query")
    
    assert "Source" in result
    assert "test_policy.pdf" in result


def test_search_policy_kb_default_k():
    """Test that search_policy_kb uses default k=5"""
    with patch('app.retrieval.cag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_policy_kb.invoke({"query": "test"})
        
        # Verify similarity_search was called with k=5
        mock_collection.similarity_search.assert_called_once()
        call_kwargs = mock_collection.similarity_search.call_args[1]
        assert call_kwargs.get('k', 5) == 5


def test_search_policy_kb_custom_k():
    """Test that search_policy_kb accepts custom k parameter"""
    with patch('app.retrieval.cag_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_policy_kb.invoke({"query": "test", "k": 10})
        
        # Verify similarity_search was called with custom k
        call_kwargs = mock_collection.similarity_search.call_args[1]
        assert call_kwargs.get('k') == 10

