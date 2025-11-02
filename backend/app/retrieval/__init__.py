"""
Retrieval implementations for knowledge base access

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/knowledge-base
Last Verified: November 2025
"""

from app.retrieval.chroma_client import (
    get_chroma_client,
    initialize_knowledge_bases,
    ChromaDBClient,
)
from app.retrieval.cag_retriever import search_policy_kb, format_policy_context
from app.retrieval.rag_retriever import search_technical_kb, format_technical_context
from app.retrieval.hybrid_retriever import search_billing_kb, get_cached_policy_info, format_billing_context

__all__ = [
    "get_chroma_client",
    "initialize_knowledge_bases",
    "ChromaDBClient",
    "search_policy_kb",
    "format_policy_context",
    "search_technical_kb",
    "format_technical_context",
    "search_billing_kb",
    "get_cached_policy_info",
    "format_billing_context",
]
