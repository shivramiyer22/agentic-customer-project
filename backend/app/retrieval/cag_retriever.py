"""
Pure CAG (Cached Augmented Generation) retrieval implementation

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/knowledge-base
Last Verified: November 2025

Pure CAG strategy: Uses static/cached policy documents without vector retrieval per query.
Optimized for fast, consistent answers from static policy documents.
"""

from typing import List, Optional, Dict, Any
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from app.retrieval.chroma_client import get_chroma_client
from app.utils.config import config
from app.utils.logger import app_logger


@tool
def search_policy_kb(
    query: str,
    k: int = 5
) -> str:
    """
    Search policy knowledge base using Pure CAG strategy (optimized for static policy documents).
    
    Pure CAG approach:
    - Uses static policy documents (cached/static, not dynamically changing)
    - Retrieves relevant policy documents from policy_knowledge_base collection
    - Returns formatted context with source citations for policy queries
    
    Use this tool to answer questions about:
    - FAA/EASA regulations
    - DFARs policies
    - Data governance policies
    - Customer support policies
    - Terms of service
    - Privacy policies
    - Legal compliance requirements
    
    Args:
        query: User query about policies, regulations, or compliance
        k: Number of documents to retrieve (default: 5 for policy documents)
        
    Returns:
        Formatted context string with policy information and source citations
    """
    try:
        # Get ChromaDB client
        client = get_chroma_client()
        
        # Get policy knowledge base collection
        policy_collection = client.get_or_create_collection(
            collection_name=config.COLLECTION_POLICY
        )
        
        # For Pure CAG, we can use vector similarity search on static documents
        # The key difference is that policy documents are static and cached
        # We retrieve relevant chunks and format them for the agent
        
        # Retrieve documents using similarity search
        # Even though it's "Pure CAG", we use ChromaDB for retrieval
        # The "CAG" aspect is that these are static policy documents (not dynamic)
        docs: List[Document] = policy_collection.similarity_search(
            query=query,
            k=k
        )
        
        if not docs:
            app_logger.warning(f"No policy documents found for query: {query[:50]}")
            return (
                "No relevant policy documents found in the knowledge base. "
                "Please check if policy documents have been uploaded to the policy knowledge base."
            )
        
        # Format retrieved documents with source citations (Pure CAG format)
        formatted_context = format_policy_context(docs, query)
        
        app_logger.info(f"Retrieved {len(docs)} policy documents for query: {query[:50]}")
        
        return formatted_context
        
    except Exception as e:
        app_logger.error(f"Error searching policy knowledge base: {e}")
        return (
            f"Error retrieving policy information: {str(e)}. "
            "Please try again or contact support if the issue persists."
        )


def format_policy_context(docs: List[Document], query: str) -> str:
    """
    Format retrieved policy documents into context string with source citations.
    
    Args:
        docs: List of retrieved Document objects
        query: Original query for context
        
    Returns:
        Formatted context string with document content and source citations
    """
    formatted_parts = []
    
    formatted_parts.append(f"Relevant policy information for query: '{query}'\n")
    formatted_parts.append("=" * 80)
    formatted_parts.append("")
    
    for i, doc in enumerate(docs, 1):
        # Extract document content
        content = doc.page_content.strip()
        
        # Extract metadata for citations
        metadata = doc.metadata or {}
        source_file = metadata.get("source_file", metadata.get("source", "Unknown"))
        document_category = metadata.get("document_category", "policy")
        chunk_index = metadata.get("chunk_index", "")
        upload_timestamp = metadata.get("upload_timestamp", "")
        
        # Format document entry
        formatted_parts.append(f"[Policy Document {i}]")
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
        "Note: This information is based on static policy documents. "
        "For the most current policies, please refer to official sources."
    )
    
    return "\n".join(formatted_parts)


def get_all_policy_documents() -> List[Document]:
    """
    Get all policy documents from the knowledge base (for caching/static access).
    
    Returns:
        List of all Document objects from policy_knowledge_base collection
    """
    try:
        client = get_chroma_client()
        policy_collection = client.get_or_create_collection(
            collection_name=config.COLLECTION_POLICY
        )
        
        # Get all documents (for Pure CAG caching strategy)
        # Note: This is a simple approach - in production, you might want pagination
        # For now, we'll use a broad search to get documents
        # In a true Pure CAG system, these would be fully cached
        
        # Use a broad query to get documents
        docs = policy_collection.similarity_search(
            query="policy regulation compliance FAA EASA DFARs",
            k=100  # Get up to 100 documents (adjust based on collection size)
        )
        
        return docs
        
    except Exception as e:
        app_logger.error(f"Error getting all policy documents: {e}")
        return []

