"""
Tests for configuration module
"""

import pytest
import os
from unittest.mock import patch
from app.utils.config import Config, config


def test_config_attributes():
    """Test that Config has all required attributes"""
    assert hasattr(Config, 'OPENAI_API_KEY')
    assert hasattr(Config, 'OPENAI_EMBEDDING_MODEL')
    assert hasattr(Config, 'OPENAI_EMBEDDING_DIMENSIONS')
    assert hasattr(Config, 'AWS_ACCESS_KEY_ID')
    assert hasattr(Config, 'AWS_SECRET_ACCESS_KEY')
    assert hasattr(Config, 'AWS_REGION')
    assert hasattr(Config, 'CHROMA_DB_PATH')
    assert hasattr(Config, 'ESCALATION_EMAIL')
    assert hasattr(Config, 'COLLECTION_BILLING')
    assert hasattr(Config, 'COLLECTION_TECHNICAL')
    assert hasattr(Config, 'COLLECTION_POLICY')


def test_config_defaults():
    """Test Config default values"""
    assert Config.OPENAI_EMBEDDING_MODEL == "text-embedding-3-small"
    assert Config.OPENAI_EMBEDDING_DIMENSIONS == 1536
    assert Config.AWS_REGION == "us-east-1"
    assert Config.CHROMA_DB_PATH == "./chroma_db"
    assert Config.COLLECTION_BILLING == "billing_knowledge_base"
    assert Config.COLLECTION_TECHNICAL == "technical_knowledge_base"
    assert Config.COLLECTION_POLICY == "policy_knowledge_base"


def test_get_all_collections():
    """Test get_all_collections method"""
    collections = Config.get_all_collections()
    assert isinstance(collections, list)
    assert len(collections) == 3
    assert "billing_knowledge_base" in collections
    assert "technical_knowledge_base" in collections
    assert "policy_knowledge_base" in collections


def test_config_validate():
    """Test Config validation"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        errors = Config.validate()
        assert isinstance(errors, list)
        # Should not have errors when OPENAI_API_KEY is set
        assert len(errors) == 0


def test_config_validate_missing_key():
    """Test Config validation with missing OPENAI_API_KEY"""
    with patch.dict(os.environ, {}, clear=True):
        with patch.object(Config, 'OPENAI_API_KEY', ''):
            errors = Config.validate()
            assert isinstance(errors, list)
            assert len(errors) > 0
            assert any("OPENAI_API_KEY" in error for error in errors)


def test_config_instance():
    """Test config instance"""
    assert config is not None
    assert isinstance(config, Config)

