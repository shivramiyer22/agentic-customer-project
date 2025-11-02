"""
Tests for document parsers
"""

import pytest
import tempfile
from pathlib import Path
from app.ingestion.parsers.pdf_parser import parse_pdf
from app.ingestion.parsers.txt_parser import parse_txt
from app.ingestion.parsers.markdown_parser import parse_markdown
from app.ingestion.parsers.json_parser import parse_json
from app.ingestion.parsers.parser_factory import get_parser, parse_document, PARSERS


def create_temp_file(content: str, suffix: str) -> Path:
    """Helper to create temporary file"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)


@pytest.fixture
def sample_txt_content():
    """Fixture for sample text content"""
    return "This is a sample text file.\nIt has multiple lines.\nFor testing purposes."


def test_get_parser_supported_formats():
    """Test get_parser with supported formats"""
    assert get_parser("test.pdf") is not None
    assert get_parser("test.txt") is not None
    assert get_parser("test.md") is not None
    assert get_parser("test.markdown") is not None
    assert get_parser("test.json") is not None


def test_get_parser_unsupported_format():
    """Test get_parser with unsupported format"""
    with pytest.raises(ValueError):
        get_parser("test.xyz")


def test_get_parser_case_insensitive():
    """Test get_parser is case insensitive"""
    assert get_parser("test.PDF") is not None
    assert get_parser("test.TXT") is not None
    assert get_parser("test.JSON") is not None


def test_parse_txt(sample_txt_content):
    """Test TXT parser"""
    file_path = create_temp_file(sample_txt_content, ".txt")
    try:
        documents = parse_txt(file_path)
        assert len(documents) > 0
        assert documents[0].page_content
        assert "sample text file" in documents[0].page_content.lower()
    finally:
        file_path.unlink()


def test_parse_json():
    """Test JSON parser"""
    content = '{"key": "value", "number": 123, "array": [1, 2, 3]}'
    file_path = create_temp_file(content, ".json")
    try:
        documents = parse_json(file_path)
        assert len(documents) > 0
        assert documents[0].page_content
        assert "key" in documents[0].page_content
        assert "value" in documents[0].page_content
    finally:
        file_path.unlink()


def test_parse_json_array():
    """Test JSON parser with array"""
    content = '[{"item": 1}, {"item": 2}, {"item": 3}]'
    file_path = create_temp_file(content, ".json")
    try:
        documents = parse_json(file_path)
        assert len(documents) > 0
        # Each array item should be a document
        assert len(documents) >= 1
    finally:
        file_path.unlink()


def test_parse_markdown():
    """Test Markdown parser"""
    content = "# Heading\n\nThis is a paragraph.\n\n## Subheading\n\nMore content."
    file_path = create_temp_file(content, ".md")
    try:
        documents = parse_markdown(file_path)
        assert len(documents) > 0
        assert documents[0].page_content
    finally:
        file_path.unlink()


def test_parse_document_factory(sample_txt_content):
    """Test parse_document factory function"""
    file_path = create_temp_file(sample_txt_content, ".txt")
    try:
        documents = parse_document(file_path)
        assert len(documents) > 0
    finally:
        file_path.unlink()


def test_parse_document_unsupported():
    """Test parse_document with unsupported format"""
    file_path = create_temp_file("content", ".xyz")
    try:
        with pytest.raises(ValueError):
            parse_document(file_path)
    finally:
        file_path.unlink()


def test_parsers_dictionary():
    """Test PARSERS dictionary"""
    assert ".pdf" in PARSERS
    assert ".txt" in PARSERS
    assert ".md" in PARSERS
    assert ".json" in PARSERS
    assert len(PARSERS) >= 4

