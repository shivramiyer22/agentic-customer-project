"""
Hybrid RAG/CAG (Retrieval-Augmented Generation / Cached Augmented Generation) retrieval implementation

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/knowledge-base
Last Verified: November 2025

Hybrid RAG/CAG strategy:
- Initial queries use RAG to retrieve dynamic information from billing_knowledge_base
- Static policy information is cached in session memory after first retrieval
- Subsequent queries in same session use cached policy data when applicable
"""

from typing import List, Optional, Dict, Any
from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain.tools import ToolRuntime
from langgraph.types import Command
from app.retrieval.chroma_client import get_chroma_client
from app.retrieval.cag_retriever import search_policy_kb
from app.utils.config import config
from app.utils.logger import app_logger


@tool
def search_billing_kb(
    query: str,
    k: int = 3
) -> str:
    """
    Search billing knowledge base using RAG strategy (dynamic vector retrieval).
    
    This tool performs dynamic RAG retrieval from billing_knowledge_base.
    Use this for billing-specific queries about pricing, invoices, contracts, etc.
    
    Use this tool to answer questions about:
    - Billing inquiries
    - Pricing questions
    - Contract terms
    - Invoices
    - Payment plans
    - Subscription changes
    - Refunds
    - Billing-related account issues
    
    Args:
        query: User query about billing, pricing, contracts, or invoices
        k: Number of documents to retrieve (default: 3 for billing documents)
        
    Returns:
        Formatted context string with billing information and source citations
    """
    try:
        # Get ChromaDB client
        client = get_chroma_client()
        
        # Get billing knowledge base collection
        billing_collection = client.get_or_create_collection(
            collection_name=config.COLLECTION_BILLING
        )
        
        # Pure RAG: Use dynamic vector similarity search for billing documents
        docs: List[Document] = billing_collection.similarity_search(
            query=query,
            k=k
        )
        
        if not docs:
            app_logger.warning(f"No billing documents found for query: {query[:50]}")
            return (
                "No relevant billing documents found in the knowledge base. "
                "Please check if billing documents have been uploaded to the billing knowledge base."
            )
        
        # Format retrieved documents with source citations (RAG format)
        formatted_context = format_billing_context(docs, query)
        
        app_logger.info(f"Retrieved {len(docs)} billing documents for query: {query[:50]}")
        
        return formatted_context
        
    except Exception as e:
        app_logger.error(f"Error searching billing knowledge base: {e}")
        return (
            f"Error retrieving billing information: {str(e)}. "
            "Please try again or contact support if the issue persists."
        )


def format_billing_context(docs: List[Document], query: str) -> str:
    """
    Format retrieved billing documents into context string with source citations.
    
    Args:
        docs: List of retrieved Document objects
        query: Original query for context
        
    Returns:
        Formatted context string with document content and source citations
    """
    formatted_parts = []
    
    formatted_parts.append(f"Relevant billing information for query: '{query}'\n")
    formatted_parts.append("=" * 80)
    formatted_parts.append("")
    
    for i, doc in enumerate(docs, 1):
        # Extract document content
        content = doc.page_content.strip()
        
        # Extract metadata for citations
        metadata = doc.metadata or {}
        source_file = metadata.get("source_file", metadata.get("source", "Unknown"))
        document_category = metadata.get("document_category", "billing")
        chunk_index = metadata.get("chunk_index", "")
        upload_timestamp = metadata.get("upload_timestamp", "")
        
        # Format document entry
        formatted_parts.append(f"[Billing Document {i}]")
        formatted_parts.append(f"Source: {source_file}")
        if upload_timestamp:
            formatted_parts.append(f"Upload Date: {upload_timestamp}")
        if chunk_index != "":
            formatted_parts.append(f"Chunk Index: {chunk_index}")
        formatted_parts.append("-" * 80)
        formatted_parts.append(content)
        formatted_parts.append("")
    
    formatted_parts.append("=" * 80)
    formatted_parts.append("")
    formatted_parts.append(
        "Note: This information is retrieved dynamically from the billing knowledge base. "
        "For the most current pricing and billing information, please refer to the latest uploaded documents."
    )
    
    return "\n".join(formatted_parts)


@tool
def get_cached_policy_info(
    query: str,
    runtime: ToolRuntime
) -> Command:
    """
    Get cached policy information from session memory (CAG strategy).
    
    This tool retrieves cached static policy information that was previously
    fetched and stored in the session state. If not cached, it fetches policy
    information and caches it for subsequent queries.
    
    Hybrid RAG/CAG approach:
    - First call: Retrieves policy info from policy_knowledge_base and caches it
    - Subsequent calls: Returns cached policy info from session state
    - Optimized for static policy documents that don't change frequently
    
    Args:
        query: Query about policies or regulations
        runtime: ToolRuntime for accessing state (injected automatically)
        
    Returns:
        Command with cached or retrieved policy information and updated state
    """
    try:
        # Check if we have cached policy info in state
        cached_policy = runtime.state.get("cached_policy_info", None)
        
        if cached_policy and query.lower() in cached_policy.get("keywords", "").lower():
            # Return cached policy info
            app_logger.info(f"Using cached policy info for query: {query[:50]}")
            return Command(
                result=cached_policy.get("content", ""),
                update={}  # State unchanged
            )
        
        # No cache or query doesn't match - retrieve from policy KB
        app_logger.info(f"Retrieving and caching policy info for query: {query[:50]}")
        
        # Use the existing policy KB search tool
        policy_info = search_policy_kb.invoke({"query": query, "k": 3})
        
        # Cache the policy info in state for subsequent queries
        cache_update = {
            "cached_policy_info": {
                "content": policy_info,
                "keywords": query.lower(),
                "cached_at": str(runtime.state.get("messages", [])[-1]) if runtime.state.get("messages") else ""
            }
        }
        
        return Command(
            result=policy_info,
            update=cache_update
        )
        
    except Exception as e:
        app_logger.error(f"Error getting cached policy info: {e}")
        # Fallback: retrieve without caching
        try:
            policy_info = search_policy_kb.invoke({"query": query, "k": 3})
            return Command(result=policy_info, update={})
        except:
            return Command(
                result=(
                    f"Error retrieving policy information: {str(e)}. "
                    "Please try again or contact support if the issue persists."
                ),
                update={}
            )

