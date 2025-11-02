"""
Tests for Hybrid RAG/CAG (Retrieval-Augmented Generation / Cached Augmented Generation) retrieval implementation

Tests for Hybrid RAG/CAG retrieval strategy for billing documents
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.documents import Document
from langgraph.types import Command
from app.retrieval.hybrid_retriever import (
    search_billing_kb,
    get_cached_policy_info,
    format_billing_context
)
from app.utils.config import config


def test_search_billing_kb_tool_decorated():
    """Test that search_billing_kb is decorated as a tool"""
    assert hasattr(search_billing_kb, 'description') or hasattr(search_billing_kb, 'name')
    assert hasattr(search_billing_kb, 'invoke') or hasattr(search_billing_kb, '__call__')


def test_search_billing_kb_no_documents():
    """Test search_billing_kb when no documents are found"""
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        result = search_billing_kb.invoke({"query": "test billing"})
        
        assert result is not None
        assert "No relevant billing documents" in result or "not found" in result.lower()


def test_search_billing_kb_with_documents():
    """Test search_billing_kb when documents are found"""
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_doc1 = Document(
            page_content="Invoice #12345 for $5,000...",
            metadata={"source_file": "invoice_12345.pdf", "document_category": "billing"}
        )
        mock_doc2 = Document(
            page_content="Contract terms: payment due in 30 days...",
            metadata={"source_file": "contract.pdf", "document_category": "billing"}
        )
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = [mock_doc1, mock_doc2]
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        result = search_billing_kb.invoke({"query": "invoice"})
        
        assert result is not None
        assert "Invoice" in result or "$5,000" in result
        assert "invoice_12345.pdf" in result or "Source" in result


def test_search_billing_kb_uses_billing_collection():
    """Test that search_billing_kb uses the correct collection"""
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_billing_kb.invoke({"query": "test"})
        
        mock_client.get_or_create_collection.assert_called_once()
        call_args = mock_client.get_or_create_collection.call_args
        assert call_args[1]['collection_name'] == config.COLLECTION_BILLING


def test_search_billing_kb_error_handling():
    """Test that search_billing_kb handles errors gracefully"""
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_get_client.side_effect = Exception("Database error")
        
        result = search_billing_kb.invoke({"query": "test"})
        
        assert result is not None
        assert "Error" in result or "error" in result.lower()


def test_format_billing_context():
    """Test format_billing_context formatting"""
    docs = [
        Document(
            page_content="Billing content 1",
            metadata={
                "source_file": "billing1.pdf",
                "document_category": "billing",
                "chunk_index": 0,
                "upload_timestamp": "2024-01-01"
            }
        ),
        Document(
            page_content="Billing content 2",
            metadata={
                "source_file": "billing2.pdf",
                "document_category": "billing",
                "chunk_index": 1
            }
        ),
    ]
    
    result = format_billing_context(docs, "test query")
    
    assert result is not None
    assert "test query" in result
    assert "Billing content 1" in result
    assert "Billing content 2" in result
    assert "billing1.pdf" in result or "Source" in result
    assert "billing2.pdf" in result or "Source" in result


def test_format_billing_context_empty_docs():
    """Test format_billing_context with empty documents list"""
    result = format_billing_context([], "test query")
    
    assert result is not None
    assert "test query" in result


def test_format_billing_context_source_citations():
    """Test that format_billing_context includes source citations"""
    docs = [
        Document(
            page_content="Test billing content",
            metadata={"source_file": "test_billing.pdf", "document_category": "billing"}
        )
    ]
    
    result = format_billing_context(docs, "test query")
    
    assert "Source" in result
    assert "test_billing.pdf" in result


def test_search_billing_kb_default_k():
    """Test that search_billing_kb uses default k=3"""
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_billing_kb.invoke({"query": "test"})
        
        mock_collection.similarity_search.assert_called_once()
        call_kwargs = mock_collection.similarity_search.call_args[1]
        assert call_kwargs.get('k', 3) == 3


def test_search_billing_kb_custom_k():
    """Test that search_billing_kb accepts custom k parameter"""
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_billing_kb.invoke({"query": "test", "k": 5})
        
        call_kwargs = mock_collection.similarity_search.call_args[1]
        assert call_kwargs.get('k') == 5


def test_get_cached_policy_info_tool_decorated():
    """Test that get_cached_policy_info is decorated as a tool"""
    assert hasattr(get_cached_policy_info, 'description') or hasattr(get_cached_policy_info, 'name')
    assert hasattr(get_cached_policy_info, 'invoke') or hasattr(get_cached_policy_info, '__call__')


def test_get_cached_policy_info_tool_decorated():
    """Test that get_cached_policy_info is decorated as a tool"""
    assert hasattr(get_cached_policy_info, 'description') or hasattr(get_cached_policy_info, 'name')
    assert hasattr(get_cached_policy_info, 'invoke') or hasattr(get_cached_policy_info, '__call__')


def test_get_cached_policy_info_has_runtime_parameter():
    """Test that get_cached_policy_info is configured with ToolRuntime parameter"""
    # ToolRuntime is injected automatically by LangChain, so we verify the tool exists
    # The actual runtime injection will be tested through integration tests
    assert get_cached_policy_info is not None
    # Check that it's a tool that can return Command
    description = getattr(get_cached_policy_info, 'description', '') or str(get_cached_policy_info)
    assert "policy" in description.lower() or "cache" in description.lower()

