"""
Markdown document parser using UnstructuredMarkdownLoader from LangChain

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/document-loaders/unstructured
Last Verified: November 2025
"""

from typing import List
from pathlib import Path
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from app.utils.logger import app_logger


def parse_markdown(file_path: str | Path) -> List[Document]:
    """
    Parse Markdown document using UnstructuredMarkdownLoader
    
    Args:
        file_path: Path to Markdown file
        
    Returns:
        List of Document objects
    """
    try:
        loader = UnstructuredMarkdownLoader(str(file_path))
        documents = loader.load()
        
        app_logger.info(f"Parsed Markdown file: {file_path} ({len(documents)} documents)")
        
        return documents
        
    except Exception as e:
        app_logger.error(f"Error parsing Markdown file {file_path}: {e}")
        raise

