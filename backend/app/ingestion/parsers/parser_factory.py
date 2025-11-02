"""
Parser factory function that selects appropriate parser based on file extension
"""

from typing import List, Callable
from pathlib import Path
from langchain_core.documents import Document

from app.ingestion.parsers.pdf_parser import parse_pdf
from app.ingestion.parsers.txt_parser import parse_txt
from app.ingestion.parsers.markdown_parser import parse_markdown
from app.ingestion.parsers.json_parser import parse_json
from app.utils.logger import app_logger


# Mapping of file extensions to parser functions
PARSERS: dict[str, Callable[[str | Path], List[Document]]] = {
    '.pdf': parse_pdf,
    '.txt': parse_txt,
    '.md': parse_markdown,
    '.markdown': parse_markdown,
    '.json': parse_json,
}


def get_parser(file_path: str | Path) -> Callable[[str | Path], List[Document]]:
    """
    Get appropriate parser function based on file extension
    
    Args:
        file_path: Path to file
        
    Returns:
        Parser function
        
    Raises:
        ValueError: If file extension is not supported
    """
    path = Path(file_path)
    extension = path.suffix.lower()
    
    if extension not in PARSERS:
        supported_extensions = ', '.join(PARSERS.keys())
        raise ValueError(
            f"Unsupported file extension: {extension}. "
            f"Supported extensions: {supported_extensions}"
        )
    
    return PARSERS[extension]


def parse_document(file_path: str | Path) -> List[Document]:
    """
    Parse document using appropriate parser based on file extension
    
    Args:
        file_path: Path to file
        
    Returns:
        List of Document objects
        
    Raises:
        ValueError: If file extension is not supported
        Exception: If parsing fails
    """
    parser = get_parser(file_path)
    return parser(file_path)

