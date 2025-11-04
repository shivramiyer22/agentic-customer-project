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
    """Test that search_billing_kb uses default k=5 (updated from k=3 for comprehensive retrieval)"""
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        search_billing_kb.invoke({"query": "test"})
        
        mock_collection.similarity_search.assert_called_once()
        call_kwargs = mock_collection.similarity_search.call_args[1]
        assert call_kwargs.get('k', 5) == 5


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


# ============================================================================
# REGRESSION TEST: Most Valuable Customer Query
# ============================================================================
# CRITICAL: This test MUST pass for any changes to the k parameter or retrieval logic.
# 
# This test ensures that comparative queries like "most valuable customer" 
# retrieve ALL invoices needed for accurate comparison. Without this, the 
# billing agent cannot correctly identify which company has the highest 
# total invoiced amount.
#
# HISTORY:
# - 2025-11-04: Regression occurred when k=5 was insufficient for comparative
#   queries. The query "Which company is our most valuable customer based on 
#   invoiced amount" failed because only 1-2 invoices were retrieved instead 
#   of all 4 invoices needed for comparison.
# - Fix: Added comparative query detection to increase k to at least 20 for
#   queries containing keywords like "most valuable", "highest", "which company", etc.
#
# REQUIREMENT:
# - The k parameter MUST NOT be changed without this test passing.
# - Any changes to search_billing_kb that affect retrieval must ensure this test passes.
# - If this test fails, the fix must restore full functionality before merging.
# ============================================================================

def test_most_valuable_customer_query_retrieves_all_invoices():
    """
    REGRESSION TEST: Most Valuable Customer Query
    
    This test ensures that the query "Which company is our most valuable customer 
    based on invoiced amount" retrieves ALL invoices needed for accurate comparison.
    
    Test Data:
    - Invoice-1-ABC-Company.pdf: INV-001, $55,000 (ABC Company)
    - Invoice-4-ABC-Company.pdf: INV-004, $357,500 (ABC Company)
    - Invoice-1-XYZ-Company.pdf: INV-002, $110,000 (XYZ Company)
    - Invoice-1-PQR-Company.pdf: INV-003, $82,500 (PQR Company)
    
    Expected Result:
    - ABC Company has 2 invoices totaling $412,500 (most valuable customer)
    - All 4 invoices must be retrieved (k >= 20 for comparative queries)
    
    CRITICAL: This test MUST pass. Do NOT change k parameter without ensuring this test passes.
    """
    # Create mock invoice documents representing the 4 invoices
    invoice_docs = [
        # ABC Company - Invoice 1
        Document(
            page_content=(
                "AEROSPACE COMPANY BILLING INVOICE\n"
                "Invoice No: INV-001\n"
                "Date: 01/01/2026\n"
                "Customer ID: ABC Company\n"
                "Subtotal: $50,000.00\n"
                "Sales Tax (10%): $5,000.00\n"
                "TOTAL DUE: $55,000.00"
            ),
            metadata={
                "source_file": "Invoice-1-ABC-Company.pdf",
                "document_category": "billing_knowledge_base",
                "chunk_index": 0
            }
        ),
        # ABC Company - Invoice 4
        Document(
            page_content=(
                "AEROSPACE COMPANY BILLING INVOICE\n"
                "Invoice No: INV-004\n"
                "Date: 01/15/2026\n"
                "Customer ID: ABC Company\n"
                "Subtotal: $325,000.00\n"
                "Sales Tax (10%): $32,500.00\n"
                "TOTAL DUE: $357,500.00"
            ),
            metadata={
                "source_file": "Invoice-4-ABC-Company.pdf",
                "document_category": "billing_knowledge_base",
                "chunk_index": 0
            }
        ),
        # XYZ Company - Invoice 1
        Document(
            page_content=(
                "AEROSPACE COMPANY BILLING INVOICE\n"
                "Invoice No: INV-002\n"
                "Date: 01/05/2026\n"
                "Customer ID: XYZ Company\n"
                "Subtotal: $100,000.00\n"
                "Sales Tax (10%): $10,000.00\n"
                "TOTAL DUE: $110,000.00"
            ),
            metadata={
                "source_file": "Invoice-1-XYZ-Company.pdf",
                "document_category": "billing_knowledge_base",
                "chunk_index": 0
            }
        ),
        # PQR Company - Invoice 1
        Document(
            page_content=(
                "AEROSPACE COMPANY BILLING INVOICE\n"
                "Invoice No: INV-003\n"
                "Date: 01/10/2026\n"
                "Customer ID: PQR Company\n"
                "Subtotal: $75,000.00\n"
                "Sales Tax (10%): $7,500.00\n"
                "TOTAL DUE: $82,500.00"
            ),
            metadata={
                "source_file": "Invoice-1-PQR-Company.pdf",
                "document_category": "billing_knowledge_base",
                "chunk_index": 0
            }
        ),
    ]
    
    # Add additional chunks for each invoice to simulate real-world scenario
    # where each invoice might have multiple chunks
    all_docs = invoice_docs.copy()
    for i in range(1, 10):  # Add 9 more chunks to simulate a larger collection
        all_docs.append(Document(
            page_content=f"Additional billing document chunk {i}",
            metadata={
                "source_file": f"other_document_{i}.pdf",
                "document_category": "billing_knowledge_base",
                "chunk_index": i
            }
        ))
    
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        
        # Mock similarity_search to return all 4 invoices when k >= 20
        # In real scenario, similarity search would rank documents, but for this test
        # we ensure all invoices are included when k is large enough
        def mock_similarity_search(query, k):
            # Return all 4 invoices first, then other documents
            if k >= 20:
                return invoice_docs + all_docs[4:4+(k-4)]
            else:
                # If k < 20, only return first 2 invoices (simulating the regression)
                return invoice_docs[:2] + all_docs[4:4+(k-2)]
        
        mock_collection.similarity_search.side_effect = mock_similarity_search
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        # Test the critical query
        query = "Which company is our most valuable customer based on invoiced amount"
        result = search_billing_kb.invoke({"query": query, "k": 5})
        
        # Verify that similarity_search was called with k >= 20 (comparative query detection)
        mock_collection.similarity_search.assert_called_once()
        call_kwargs = mock_collection.similarity_search.call_args[1]
        actual_k = call_kwargs.get('k', 5)
        
        # CRITICAL ASSERTION: k must be >= 20 for comparative queries
        assert actual_k >= 20, (
            f"CRITICAL REGRESSION: Comparative query must use k >= 20, but got k={actual_k}. "
            f"This will cause incomplete invoice retrieval. "
            f"DO NOT change k parameter without ensuring this test passes."
        )
        
        # Verify that all 4 invoices are present in the result
        invoice_files = [
            "Invoice-1-ABC-Company.pdf",
            "Invoice-4-ABC-Company.pdf",
            "Invoice-1-XYZ-Company.pdf",
            "Invoice-1-PQR-Company.pdf"
        ]
        
        found_invoices = [f for f in invoice_files if f in result]
        
        assert len(found_invoices) == 4, (
            f"CRITICAL REGRESSION: All 4 invoices must be retrieved, but only found {len(found_invoices)}. "
            f"Found: {found_invoices}, Missing: {set(invoice_files) - set(found_invoices)}. "
            f"This will cause incorrect 'most valuable customer' identification. "
            f"DO NOT change k parameter or retrieval logic without ensuring this test passes."
        )
        
        # Verify that ABC Company's invoices are present (most valuable customer)
        assert "Invoice-1-ABC-Company.pdf" in result, (
            "CRITICAL: ABC Company invoice 1 must be retrieved for accurate comparison"
        )
        assert "Invoice-4-ABC-Company.pdf" in result, (
            "CRITICAL: ABC Company invoice 4 must be retrieved for accurate comparison"
        )
        
        # Verify that invoice amounts are present
        assert "$55,000" in result or "$55,000.00" in result or "55,000" in result, (
            "ABC Company invoice 1 amount ($55,000) must be present"
        )
        assert "$357,500" in result or "$357,500.00" in result or "357,500" in result, (
            "ABC Company invoice 4 amount ($357,500) must be present"
        )


def test_comparative_query_detection_increases_k():
    """
    Test that comparative queries automatically increase k to at least 20.
    
    This ensures that queries like "most valuable", "highest", "which company"
    retrieve enough documents for accurate comparison.
    """
    comparative_queries = [
        "Which company is our most valuable customer based on invoiced amount",
        "What is the highest invoice amount?",
        "Which customer has the largest total?",
        "Show me all companies and their invoice totals",
        "Compare all customer invoices",
    ]
    
    with patch('app.retrieval.hybrid_retriever.get_chroma_client') as mock_get_client:
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.similarity_search.return_value = []
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_get_client.return_value = mock_client
        
        for query in comparative_queries:
            mock_collection.similarity_search.reset_mock()
            search_billing_kb.invoke({"query": query, "k": 5})
            
            # Verify that k was increased to at least 20
            call_kwargs = mock_collection.similarity_search.call_args[1]
            actual_k = call_kwargs.get('k', 5)
            assert actual_k >= 20, (
                f"Comparative query '{query}' must use k >= 20, but got k={actual_k}"
            )

