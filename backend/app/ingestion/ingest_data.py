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
    "technical", "tech", "specification", "manual", "bug", "issue", "defect",
    "engineering", "component", "system", "hardware", "software",
    "spec", "design", "documentation", "troubleshooting", "repair",
    "maintenance", "service bulletin", "publication", "bug-report", "bug_report",
    "bug report", "technical report", "tech report"
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
    (billing, technical, or policy) based on comprehensive content analysis
    
    This function performs:
    1. Keyword-based scoring (filename and content)
    2. Content structure analysis (headings, sections, title)
    3. Keyword context analysis (surrounding words)
    4. Overall theme detection
    5. Full document review when multiple categories are present
    
    Args:
        content: Document content text
        filename: Optional filename for additional context
        
    Returns:
        Collection name: billing_knowledge_base, technical_knowledge_base, or policy_knowledge_base
    """
    import re
    
    content_lower = content.lower()
    filename_lower = filename.lower()
    content_words = content_lower.split()
    total_words = len(content_words)
    
    # Initialize scores
    billing_score = 0
    technical_score = 0
    policy_score = 0
    
    # Step 1: Filename analysis (strong indicator, give 3x weight and priority)
    if filename_lower:
        # Check for strong filename patterns first (highest priority)
        # Technical patterns (case-insensitive, check various formats)
        technical_patterns = [
            "tech-", "tech_", "bug-", "bug_", "technical-", "technical_",
            "tech-bug", "tech_bug", "bug-report", "bug_report", "bugreport",
            "technical-report", "technical_report", "techreport"
        ]
        if any(pattern in filename_lower for pattern in technical_patterns):
            technical_score += 10  # Very strong technical indicator
            app_logger.info(f"Strong technical filename pattern detected in: {filename}")
        
        # Billing patterns
        billing_patterns = [
            "billing", "invoice", "price", "contract-", "contract_",
            "billing-", "invoice-", "price-", "pricing-"
        ]
        if any(pattern in filename_lower for pattern in billing_patterns):
            billing_score += 10  # Very strong billing indicator
            app_logger.info(f"Strong billing filename pattern detected in: {filename}")
        
        # Policy patterns
        policy_patterns = [
            "policy", "compliance", "regulation", "faa", "easa",
            "policy-", "compliance-", "regulation-"
        ]
        if any(pattern in filename_lower for pattern in policy_patterns):
            policy_score += 10  # Very strong policy indicator
            app_logger.info(f"Strong policy filename pattern detected in: {filename}")
        
        # Then check keyword matches (lower weight since patterns are more specific)
        billing_score += sum(1 for keyword in BILLING_KEYWORDS if keyword in filename_lower)
        technical_score += sum(1 for keyword in TECHNICAL_KEYWORDS if keyword in filename_lower)
        policy_score += sum(1 for keyword in POLICY_KEYWORDS if keyword in filename_lower)
    
    # Step 2: Content structure analysis (headings, title, sections)
    # Extract potential headings (lines that are short and likely headings)
    lines = content.split('\n')
    headings = []
    for line in lines[:50]:  # Check first 50 lines for headings
        line_stripped = line.strip()
        if len(line_stripped) > 0 and len(line_stripped) < 100:
            # Check if line looks like a heading (short, may have special chars, or all caps)
            if (line_stripped.isupper() or 
                line_stripped.startswith('#') or 
                line_stripped.startswith('=') or
                any(char in line_stripped for char in [':', ' - ', ' – '])):
                headings.append(line_stripped.lower())
    
    # Analyze headings for category indicators
    headings_text = ' '.join(headings)
    if headings_text:
        billing_score += sum(1.5 for keyword in BILLING_KEYWORDS if keyword in headings_text)
        technical_score += sum(1.5 for keyword in TECHNICAL_KEYWORDS if keyword in headings_text)
        policy_score += sum(1.5 for keyword in POLICY_KEYWORDS if keyword in headings_text)
    
    # Step 3: Keyword frequency and density analysis
    # Count keyword occurrences in full content
    billing_keyword_count = sum(content_lower.count(keyword) for keyword in BILLING_KEYWORDS)
    technical_keyword_count = sum(content_lower.count(keyword) for keyword in TECHNICAL_KEYWORDS)
    policy_keyword_count = sum(content_lower.count(keyword) for keyword in POLICY_KEYWORDS)
    
    # Add scores based on keyword frequency (normalized by document length)
    if total_words > 0:
        billing_score += (billing_keyword_count / total_words) * 100
        technical_score += (technical_keyword_count / total_words) * 100
        policy_score += (policy_keyword_count / total_words) * 100
    
    # Step 4: Keyword context analysis (check surrounding words)
    # Look for context around keywords to understand document theme
    for keyword in BILLING_KEYWORDS:
        if keyword in content_lower:
            # Find context around keyword occurrences
            pattern = re.compile(r'.{0,50}' + re.escape(keyword) + r'.{0,50}', re.IGNORECASE)
            matches = pattern.findall(content_lower)
            for match in matches:
                # Check if surrounding context suggests billing theme
                if any(ctx in match for ctx in ['invoice', 'payment', 'price', 'cost', 'billing', 'contract']):
                    billing_score += 0.5
    
    for keyword in TECHNICAL_KEYWORDS:
        if keyword in content_lower:
            pattern = re.compile(r'.{0,50}' + re.escape(keyword) + r'.{0,50}', re.IGNORECASE)
            matches = pattern.findall(content_lower)
            for match in matches:
                if any(ctx in match for ctx in ['bug', 'issue', 'defect', 'technical', 'specification', 'component', 'system']):
                    technical_score += 0.5
    
    for keyword in POLICY_KEYWORDS:
        if keyword in content_lower:
            pattern = re.compile(r'.{0,50}' + re.escape(keyword) + r'.{0,50}', re.IGNORECASE)
            matches = pattern.findall(content_lower)
            for match in matches:
                if any(ctx in match for ctx in ['policy', 'regulation', 'compliance', 'faa', 'easa', 'legal']):
                    policy_score += 0.5
    
    # Step 5: Full document review when multiple categories are present
    # If document has significant keywords from multiple categories, analyze overall theme
    has_multiple_categories = (
        (billing_keyword_count > 0 and technical_keyword_count > 0) or
        (billing_keyword_count > 0 and policy_keyword_count > 0) or
        (technical_keyword_count > 0 and policy_keyword_count > 0)
    )
    
    if has_multiple_categories and total_words > 100:
        # Analyze document sections to determine primary theme
        # Split document into sections (by paragraphs or double newlines)
        sections = re.split(r'\n\s*\n+', content)
        
        # Analyze each section for dominant category
        section_scores = {'billing': 0, 'technical': 0, 'policy': 0}
        for section in sections[:20]:  # Analyze first 20 sections
            section_lower = section.lower()
            section_billing = sum(1 for kw in BILLING_KEYWORDS if kw in section_lower)
            section_technical = sum(1 for kw in TECHNICAL_KEYWORDS if kw in section_lower)
            section_policy = sum(1 for kw in POLICY_KEYWORDS if kw in section_lower)
            
            if section_billing > section_technical and section_billing > section_policy:
                section_scores['billing'] += len(section.split())
            elif section_technical > section_billing and section_technical > section_policy:
                section_scores['technical'] += len(section.split())
            elif section_policy > section_billing and section_policy > section_technical:
                section_scores['policy'] += len(section.split())
        
        # Add weighted scores based on section analysis
        total_section_words = sum(section_scores.values())
        if total_section_words > 0:
            billing_score += (section_scores['billing'] / total_section_words) * 20
            technical_score += (section_scores['technical'] / total_section_words) * 20
            policy_score += (section_scores['policy'] / total_section_words) * 20
        
        # Analyze document title/first paragraph (strong indicator of document purpose)
        first_paragraph = content[:500].lower() if len(content) > 500 else content_lower
        first_paragraph_billing = sum(1 for kw in BILLING_KEYWORDS if kw in first_paragraph)
        first_paragraph_technical = sum(1 for kw in TECHNICAL_KEYWORDS if kw in first_paragraph)
        first_paragraph_policy = sum(1 for kw in POLICY_KEYWORDS if kw in first_paragraph)
        
        if first_paragraph_billing > first_paragraph_technical and first_paragraph_billing > first_paragraph_policy:
            billing_score += 5
        elif first_paragraph_technical > first_paragraph_billing and first_paragraph_technical > first_paragraph_policy:
            technical_score += 5
        elif first_paragraph_policy > first_paragraph_billing and first_paragraph_policy > first_paragraph_technical:
            policy_score += 5
    
    # Step 6: Determine category based on highest score
    # Give priority to filename patterns if they strongly indicate a category
    filename_strong_indicator = None
    if filename_lower:
        # Check if filename has very strong indicators
        if any(pattern in filename_lower for pattern in ["tech-", "tech_", "bug-", "bug_", "technical-", "technical_", "tech-bug", "tech_bug", "bug-report", "bug_report"]):
            filename_strong_indicator = "technical"
        elif any(pattern in filename_lower for pattern in ["billing", "invoice", "price", "contract-", "contract_", "billing-", "invoice-"]):
            filename_strong_indicator = "billing"
        elif any(pattern in filename_lower for pattern in ["policy", "compliance", "regulation", "faa", "easa", "policy-", "compliance-"]):
            filename_strong_indicator = "policy"
    
    app_logger.info(
        f"Document categorization scores for '{filename}': "
        f"Billing={billing_score:.2f}, Technical={technical_score:.2f}, Policy={policy_score:.2f}, "
        f"Filename strong indicator={filename_strong_indicator}"
    )
    
    # Determine category - if filename has strong indicator, use it unless content strongly contradicts
    if filename_strong_indicator == "technical":
        # Filename strongly indicates technical - use technical unless billing score is much higher
        if technical_score >= billing_score * 0.7:  # Allow technical if it's at least 70% of billing score
            return config.COLLECTION_TECHNICAL
        elif billing_score > technical_score * 1.5:  # Only use billing if it's 50%+ higher
            app_logger.warning(f"Filename indicates technical but content suggests billing - using technical based on filename")
            return config.COLLECTION_TECHNICAL
        else:
            return config.COLLECTION_TECHNICAL
    elif filename_strong_indicator == "billing":
        if billing_score >= technical_score * 0.7:
            return config.COLLECTION_BILLING
        elif technical_score > billing_score * 1.5:
            app_logger.warning(f"Filename indicates billing but content suggests technical - using billing based on filename")
            return config.COLLECTION_BILLING
        else:
            return config.COLLECTION_BILLING
    elif filename_strong_indicator == "policy":
        if policy_score >= billing_score * 0.7 and policy_score >= technical_score * 0.7:
            return config.COLLECTION_POLICY
        elif billing_score > policy_score * 1.5 or technical_score > policy_score * 1.5:
            app_logger.warning(f"Filename indicates policy but content suggests other category - using policy based on filename")
            return config.COLLECTION_POLICY
        else:
            return config.COLLECTION_POLICY
    
    # No strong filename indicator - use score-based logic
    if policy_score > billing_score and policy_score > technical_score:
        return config.COLLECTION_POLICY
    elif technical_score > billing_score and technical_score > policy_score:
        return config.COLLECTION_TECHNICAL
    elif billing_score > technical_score and billing_score > policy_score:
        return config.COLLECTION_BILLING
    elif technical_score == billing_score and technical_score > policy_score:
        # Tie between technical and billing - prefer technical
        return config.COLLECTION_TECHNICAL
    elif technical_score == policy_score and technical_score > billing_score:
        # Tie between technical and policy - prefer technical
        return config.COLLECTION_TECHNICAL
    elif billing_score == policy_score and billing_score > technical_score:
        # Tie between billing and policy - prefer policy
        return config.COLLECTION_POLICY
    else:
        # Default fallback: prefer technical over billing
        return config.COLLECTION_TECHNICAL


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

