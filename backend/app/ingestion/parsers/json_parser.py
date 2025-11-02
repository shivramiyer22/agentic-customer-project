"""
JSON document parser

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/document-loaders/json
Last Verified: November 2025
"""

from typing import List, Any, Dict
from pathlib import Path
import json
from langchain_core.documents import Document
from app.utils.logger import app_logger


def parse_json(file_path: str | Path) -> List[Document]:
    """
    Parse JSON document
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        List of Document objects
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = []
        
        # Handle different JSON structures
        if isinstance(data, dict):
            # Convert dict to string representation
            content = json.dumps(data, indent=2)
            documents.append(
                Document(
                    page_content=content,
                    metadata={"source": str(file_path), "type": "json_object"}
                )
            )
        elif isinstance(data, list):
            # Process each item in the list
            for i, item in enumerate(data):
                content = json.dumps(item, indent=2)
                documents.append(
                    Document(
                        page_content=content,
                        metadata={"source": str(file_path), "type": "json_array_item", "index": i}
                    )
                )
        else:
            # Handle primitive types
            content = str(data)
            documents.append(
                Document(
                    page_content=content,
                    metadata={"source": str(file_path), "type": "json_primitive"}
                )
            )
        
        app_logger.info(f"Parsed JSON file: {file_path} ({len(documents)} documents)")
        
        return documents
        
    except json.JSONDecodeError as e:
        app_logger.error(f"JSON decode error for file {file_path}: {e}")
        raise
    except Exception as e:
        app_logger.error(f"Error parsing JSON file {file_path}: {e}")
        raise

