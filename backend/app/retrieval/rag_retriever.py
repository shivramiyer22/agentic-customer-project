"""
Pure RAG (Retrieval-Augmented Generation) retrieval implementation

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/knowledge-base
Last Verified: November 2025

Pure RAG strategy: Uses dynamic vector retrieval to fetch relevant documents from knowledge base.
Optimized for dynamic, changing technical documentation, bug reports, and specifications.
"""

from typing import List, Optional, Dict, Any
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from app.retrieval.chroma_client import get_chroma_client
from app.utils.config import config
from app.utils.logger import app_logger


@tool
def search_technical_kb(
    query: str,
    k: int = 3
) -> str:
    """
    Search technical knowledge base using Pure RAG strategy (dynamic vector retrieval).
    
    Pure RAG approach:
    - Uses dynamic vector similarity search to retrieve relevant documents
    - Retrieves top k documents from technical_knowledge_base collection
    - Returns formatted context with document names and excerpts for technical queries
    
    Use this tool to answer questions about:
    - Technical documentation
    - Component specifications
    - Bug reports
    - Technical manuals
    - Troubleshooting guides
    - Engineering questions
    - System documentation
    - API documentation
    
    Args:
        query: User query about technical topics, documentation, or specifications
        k: Number of documents to retrieve (default: 3 for technical documents)
        
    Returns:
        Formatted context string with technical information and source citations
    """
    try:
        # Get ChromaDB client
        client = get_chroma_client()
        
        # Get technical knowledge base collection
        technical_collection = client.get_or_create_collection(
            collection_name=config.COLLECTION_TECHNICAL
        )
        
        # Pure RAG: Use dynamic vector similarity search
        # This retrieves the most relevant documents based on the query
        docs: List[Document] = technical_collection.similarity_search(
            query=query,
            k=k
        )
        
        if not docs:
            app_logger.warning(f"No technical documents found for query: {query[:50]}")
            return (
                "No relevant technical documents found in the knowledge base. "
                "Please check if technical documents have been uploaded to the technical knowledge base."
            )
        
        # Format retrieved documents with source citations (Pure RAG format)
        formatted_context = format_technical_context(docs, query)
        
        app_logger.info(f"Retrieved {len(docs)} technical documents for query: {query[:50]}")
        
        return formatted_context
        
    except Exception as e:
        app_logger.error(f"Error searching technical knowledge base: {e}")
        return (
            f"Error retrieving technical information: {str(e)}. "
            "Please try again or contact support if the issue persists."
        )


def format_technical_context(docs: List[Document], query: str) -> str:
    """
    Format retrieved technical documents into context string with source citations.
    
    Args:
        docs: List of retrieved Document objects
        query: Original query for context
        
    Returns:
        Formatted context string with document content and source citations
    """
    formatted_parts = []
    
    formatted_parts.append(f"Relevant technical information for query: '{query}'\n")
    formatted_parts.append("=" * 80)
    formatted_parts.append("")
    
    for i, doc in enumerate(docs, 1):
        # Extract document content
        content = doc.page_content.strip()
        
        # Extract metadata for citations
        metadata = doc.metadata or {}
        source_file = metadata.get("source_file", metadata.get("source", "Unknown"))
        document_category = metadata.get("document_category", "technical")
        chunk_index = metadata.get("chunk_index", "")
        upload_timestamp = metadata.get("upload_timestamp", "")
        
        # Format document entry
        formatted_parts.append(f"[Technical Document {i}]")
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
        "Note: This information is retrieved dynamically from the technical knowledge base. "
        "For the most current documentation, please refer to the latest uploaded documents."
    )
    
    return "\n".join(formatted_parts)





