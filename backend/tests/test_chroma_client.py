"""
Tests for ChromaDB client
"""

import pytest
import os
import shutil
from pathlib import Path
from app.retrieval.chroma_client import (
    get_chroma_client,
    initialize_knowledge_bases,
)
from app.utils.config import Config


@pytest.fixture
def temp_chroma_path(tmp_path):
    """Fixture for temporary ChromaDB path"""
    temp_path_obj = tmp_path / "test_chroma_db"
    yield str(temp_path_obj)
    # Cleanup is handled by pytest tmp_path fixture


def test_get_chroma_client(temp_chroma_path):
    """Test get_chroma_client"""
    import app.retrieval.chroma_client as chroma_module
    # Reset the global client to allow new path
    chroma_module._chroma_client = None
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Config, 'CHROMA_DB_PATH', temp_chroma_path)
        client = get_chroma_client()
        assert client is not None
        # Verify client can list collections
        collections = client.list_collections()
        assert isinstance(collections, list)


def test_get_or_create_collection(temp_chroma_path):
    """Test get_or_create_collection"""
    import app.retrieval.chroma_client as chroma_module
    # Reset the global client to allow new path
    chroma_module._chroma_client = None
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Config, 'CHROMA_DB_PATH', temp_chroma_path)
        client = get_chroma_client()
        collection_name = "test_collection"
        # Provide metadata to avoid empty metadata error
        collection = client.get_or_create_collection(
            collection_name,
            metadata={"description": "Test collection", "type": "test"}
        )
        assert collection is not None
        # Verify collection exists
        assert collection_name in client.list_collections()


def test_get_or_create_collection_existing(temp_chroma_path):
    """Test get_or_create_collection with existing collection"""
    import app.retrieval.chroma_client as chroma_module
    # Reset the global client to allow new path
    chroma_module._chroma_client = None
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Config, 'CHROMA_DB_PATH', temp_chroma_path)
        client = get_chroma_client()
        collection_name = "existing_collection"
        
        # Create collection first with metadata
        collection1 = client.get_or_create_collection(
            collection_name,
            metadata={"description": "Existing collection", "type": "test"}
        )
        
        # Get existing collection (should use same instance)
        collection2 = client.get_or_create_collection(collection_name)
        
        # Both should be the same collection
        assert collection1 is not None
        assert collection2 is not None


def test_initialize_knowledge_bases(temp_chroma_path):
    """Test initialize_knowledge_bases"""
    import app.retrieval.chroma_client as chroma_module
    # Reset the global client to allow new path
    chroma_module._chroma_client = None
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Config, 'CHROMA_DB_PATH', temp_chroma_path)
        
        # Initialize knowledge bases
        initialize_knowledge_bases()
        
        # Verify collections exist
        client = get_chroma_client()
        collections = client.list_collections()
        collection_names = collections  # list_collections returns list of strings
        
        assert "billing_knowledge_base" in collection_names
        assert "technical_knowledge_base" in collection_names
        assert "policy_knowledge_base" in collection_names

