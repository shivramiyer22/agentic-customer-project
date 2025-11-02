"""
Plain text document parser using TextLoader from LangChain

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/document-loaders/text
Last Verified: November 2025
"""

from typing import List
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from app.utils.logger import app_logger


def parse_txt(file_path: str | Path) -> List[Document]:
    """
    Parse plain text document using TextLoader
    
    Args:
        file_path: Path to text file
        
    Returns:
        List of Document objects
    """
    try:
        loader = TextLoader(str(file_path), encoding='utf-8')
        documents = loader.load()
        
        app_logger.info(f"Parsed TXT file: {file_path} ({len(documents)} documents)")
        
        return documents
        
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            loader = TextLoader(str(file_path), encoding='latin-1')
            documents = loader.load()
            app_logger.info(f"Parsed TXT file with latin-1 encoding: {file_path} ({len(documents)} documents)")
            return documents
        except Exception as e:
            app_logger.error(f"Error parsing TXT file {file_path}: {e}")
            raise
    except Exception as e:
        app_logger.error(f"Error parsing TXT file {file_path}: {e}")
        raise

