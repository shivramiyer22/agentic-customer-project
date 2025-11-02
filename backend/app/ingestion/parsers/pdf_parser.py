"""
PDF document parser using PyPDFLoader from LangChain

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/document-loaders/pdf
Last Verified: November 2025
"""

from typing import List
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from app.utils.logger import app_logger


def parse_pdf(file_path: str | Path) -> List[Document]:
    """
    Parse PDF document using PyPDFLoader
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        List of Document objects
    """
    try:
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        
        app_logger.info(f"Parsed PDF file: {file_path} ({len(documents)} pages)")
        
        return documents
        
    except Exception as e:
        app_logger.error(f"Error parsing PDF file {file_path}: {e}")
        raise

