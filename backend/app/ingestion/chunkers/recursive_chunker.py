"""
Recursive character text chunker using RecursiveCharacterTextSplitter from LangChain

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/text-splitters/recursive-character
Last Verified: November 2025
"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.utils.config import config
from app.utils.logger import app_logger


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """
    Chunk documents using RecursiveCharacterTextSplitter
    
    Args:
        documents: List of Document objects to chunk
        chunk_size: Maximum size of each chunk (default: 1000)
        chunk_overlap: Overlap between chunks (default: 200)
        
    Returns:
        List of chunked Document objects
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        
        chunks = text_splitter.split_documents(documents)
        
        app_logger.info(
            f"Chunked {len(documents)} documents into {len(chunks)} chunks "
            f"(chunk_size={chunk_size}, chunk_overlap={chunk_overlap})"
        )
        
        return chunks
        
    except Exception as e:
        app_logger.error(f"Error chunking documents: {e}")
        raise

