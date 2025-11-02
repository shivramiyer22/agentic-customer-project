"""
Document parsers package initialization
"""

from app.ingestion.parsers.parser_factory import (
    parse_document,
    get_parser,
    PARSERS,
)

__all__ = ["parse_document", "get_parser", "PARSERS"]

