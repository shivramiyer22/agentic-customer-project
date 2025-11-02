"""
Pytest configuration and fixtures
"""

import pytest
import os
from pathlib import Path


@pytest.fixture
def test_data_dir():
    """Fixture for test data directory"""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def temp_dir():
    """Fixture for temporary directory"""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text_file(temp_dir):
    """Fixture for sample text file"""
    file_path = temp_dir / "sample.txt"
    file_path.write_text("This is a sample text file for testing.")
    return file_path


@pytest.fixture
def sample_pdf_content():
    """Fixture for sample PDF content (simplified for testing)"""
    # In real tests, you'd use actual PDF bytes
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\ntrailer\n<<\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF"

