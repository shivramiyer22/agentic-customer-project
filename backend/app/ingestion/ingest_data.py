"""
Main document ingestion pipeline

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/document-loaders
Last Verified: November 2025
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from langchain_core.documents import Document

from app.ingestion.parsers.parser_factory import parse_document
from app.ingestion.chunkers.recursive_chunker import chunk_documents
from app.retrieval.chroma_client import get_chroma_client
from app.utils.config import config
from app.utils.logger import app_logger


# Auto-Map keyword patterns for categorization
BILLING_KEYWORDS = [
    "billing", "invoice", "payment", "price", "cost", "pricing",
    "contract", "purchase order", "quote", "invoice", "billing",
    "revenue", "charge", "fee", "rate", "tariff", "catalog", "parts catalog"
]

TECHNICAL_KEYWORDS = [
    "technical", "specification", "manual", "bug", "issue", "defect",
    "engineering", "component", "system", "hardware", "software",
    "spec", "design", "documentation", "troubleshooting", "repair",
    "maintenance", "service bulletin", "publication"
]

POLICY_KEYWORDS = [
    "policy", "regulation", "compliance", "FAA", "EASA", "DFARs",
    "government", "regulatory", "legal", "standard", "procedure",
    "governance", "data governance", "customer support policy",
    "service level", "aging", "invoicing policy", "defense", "commercial"
]


def categorize_document(content: str, filename: str = "") -> str:
    """
    Analyze document content to determine appropriate knowledge base
    (billing, technical, or policy) based on keywords and content analysis
    
    Args:
        content: Document content text
        filename: Optional filename for additional context
        
    Returns:
        Collection name: billing_knowledge_base, technical_knowledge_base, or policy_knowledge_base
    """
    content_lower = content.lower()
    filename_lower = filename.lower()
    
    # Count keyword matches
    billing_score = sum(1 for keyword in BILLING_KEYWORDS if keyword in content_lower or keyword in filename_lower)
    technical_score = sum(1 for keyword in TECHNICAL_KEYWORDS if keyword in content_lower or keyword in filename_lower)
    policy_score = sum(1 for keyword in POLICY_KEYWORDS if keyword in content_lower or keyword in filename_lower)
    
    # Determine category based on highest score
    if policy_score > billing_score and policy_score > technical_score:
        return config.COLLECTION_POLICY
    elif technical_score > billing_score:
        return config.COLLECTION_TECHNICAL
    else:
        return config.COLLECTION_BILLING


def validate_file(file_path: str | Path) -> tuple[bool, Optional[str]]:
    """
    Validate file format, size, and corruption
    
    Args:
        file_path: Path to file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, f"File does not exist: {file_path}"
        
        # Check file extension
        extension = path.suffix.lower()
        supported_extensions = ['.pdf', '.txt', '.md', '.markdown', '.json']
        if extension not in supported_extensions:
            return False, f"Unsupported file format: {extension}. Supported: {supported_extensions}"
        
        # Check file size (target: average 100 KB, max validation)
        file_size = path.stat().st_size
        max_file_size = 20 * 1024 * 1024  # 20 MB max per file
        
        if file_size == 0:
            return False, "File is empty"
        
        if file_size > max_file_size:
            return False, f"File size ({file_size / 1024 / 1024:.2f} MB) exceeds maximum allowed size ({max_file_size / 1024 / 1024:.2f} MB)"
        
        # Basic corruption check: try to open file
        try:
            with open(path, 'rb') as f:
                f.read(1)
        except Exception as e:
            return False, f"File appears to be corrupted or unreadable: {e}"
        
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {e}"


def enrich_metadata(
    documents: List[Document],
    source_file: str | Path,
    document_category: str,
    upload_timestamp: Optional[datetime] = None,
) -> List[Document]:
    """
    Add metadata enrichment to documents
    
    Args:
        documents: List of Document objects
        source_file: Source file path
        document_category: Document category (billing, technical, policy)
        upload_timestamp: Upload timestamp (default: current time)
        
    Returns:
        List of Document objects with enriched metadata
    """
    if upload_timestamp is None:
        upload_timestamp = datetime.utcnow()
    
    source_path = Path(source_file)
    source_name = source_path.name
    
    enriched_documents = []
    
    for i, doc in enumerate(documents):
        # Preserve existing metadata
        metadata = doc.metadata.copy()
        
        # Add new metadata
        metadata.update({
            "source_file": source_name,
            "source_path": str(source_path),
            "upload_timestamp": upload_timestamp.isoformat(),
            "document_category": document_category,
            "chunk_index": i,
            "total_chunks": len(documents),
        })
        
        enriched_documents.append(
            Document(
                page_content=doc.page_content,
                metadata=metadata,
            )
        )
    
    return enriched_documents


def ingest_document(
    file_path: str | Path,
    target_collection: Optional[str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    auto_map: bool = False,
) -> Dict[str, Any]:
    """
    Main ingestion pipeline: parse, chunk, generate embeddings, and store in ChromaDB
    
    Args:
        file_path: Path to file to ingest
        target_collection: Target ChromaDB collection name (None for auto-map)
        chunk_size: Chunk size for text splitting (default: 1000)
        chunk_overlap: Chunk overlap for text splitting (default: 200)
        auto_map: Whether to auto-categorize document (default: False)
        
    Returns:
        Dictionary with ingestion results
    """
    start_time = datetime.utcnow()
    source_path = Path(file_path)
    
    try:
        # Step 1: Validate file
        app_logger.info(f"Validating file: {source_path}")
        is_valid, error = validate_file(source_path)
        if not is_valid:
            raise ValueError(f"File validation failed: {error}")
        
        # Step 2: Parse document
        app_logger.info(f"Parsing document: {source_path}")
        documents = parse_document(source_path)
        
        if not documents:
            raise ValueError("No documents extracted from file")
        
        # Step 3: Determine target collection
        if auto_map or target_collection is None:
            # Auto-categorize based on content
            content = "\n".join([doc.page_content for doc in documents])
            target_collection = categorize_document(content, source_path.name)
            app_logger.info(f"Auto-categorized document to: {target_collection}")
        else:
            # Use provided target collection
            app_logger.info(f"Using provided target collection: {target_collection}")
        
        # Validate target collection
        if target_collection not in config.get_all_collections():
            raise ValueError(
                f"Invalid target collection: {target_collection}. "
                f"Valid collections: {config.get_all_collections()}"
            )
        
        # Step 4: Chunk documents
        app_logger.info(f"Chunking documents (chunk_size={chunk_size}, chunk_overlap={chunk_overlap})")
        chunks = chunk_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        # Step 5: Enrich metadata
        app_logger.info("Enriching metadata")
        enriched_chunks = enrich_metadata(
            chunks,
            source_path,
            target_collection,
            start_time,
        )
        
        # Step 6: Get ChromaDB collection
        app_logger.info(f"Getting ChromaDB collection: {target_collection}")
        client = get_chroma_client()
        vectorstore = client.get_or_create_collection(target_collection)
        
        # Step 7: Store vectors in ChromaDB
        app_logger.info(f"Storing {len(enriched_chunks)} chunks in ChromaDB")
        vectorstore.add_documents(enriched_chunks)
        
        # Persist to disk
        vectorstore.persist()
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        result = {
            "success": True,
            "file_path": str(source_path),
            "file_name": source_path.name,
            "target_collection": target_collection,
            "documents_count": len(documents),
            "chunks_count": len(enriched_chunks),
            "duration_seconds": duration,
            "upload_timestamp": start_time.isoformat(),
        }
        
        app_logger.info(
            f"Successfully ingested {source_path.name}: "
            f"{len(enriched_chunks)} chunks stored in {target_collection} "
            f"({duration:.2f}s)"
        )
        
        return result
        
    except ValueError as e:
        app_logger.error(f"Validation error ingesting {source_path}: {e}")
        raise
    except Exception as e:
        app_logger.error(f"Error ingesting {source_path}: {e}")
        raise


def ingest_multiple_documents(
    file_paths: List[str | Path],
    target_collection: Optional[str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    auto_map: bool = False,
) -> List[Dict[str, Any]]:
    """
    Ingest multiple documents
    
    Args:
        file_paths: List of file paths to ingest
        target_collection: Target ChromaDB collection name (None for auto-map)
        chunk_size: Chunk size for text splitting
        chunk_overlap: Chunk overlap for text splitting
        auto_map: Whether to auto-categorize documents
        
    Returns:
        List of ingestion results
    """
    results = []
    
    for file_path in file_paths:
        try:
            result = ingest_document(
                file_path=file_path,
                target_collection=target_collection,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                auto_map=auto_map,
            )
            results.append(result)
        except Exception as e:
            app_logger.error(f"Failed to ingest {file_path}: {e}")
            results.append({
                "success": False,
                "file_path": str(file_path),
                "error": str(e),
            })
    
    return results

