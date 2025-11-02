"""
Tests for conversation state management

Tests for InMemorySaver checkpointer and conversation persistence
"""

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from app.state.conversation_state import get_checkpointer


def test_get_checkpointer():
    """Test that get_checkpointer returns InMemorySaver instance"""
    checkpointer = get_checkpointer()
    
    assert checkpointer is not None
    assert isinstance(checkpointer, InMemorySaver)


def test_checkpointer_singleton():
    """Test that get_checkpointer returns same instance (singleton pattern)"""
    checkpointer1 = get_checkpointer()
    checkpointer2 = get_checkpointer()
    
    assert checkpointer1 is checkpointer2


def test_checkpointer_type():
    """Test that checkpointer is correct type"""
    checkpointer = get_checkpointer()
    
    # InMemorySaver is from langgraph.checkpoint.memory
    assert hasattr(checkpointer, 'list')
    assert hasattr(checkpointer, 'put')
    assert hasattr(checkpointer, 'get')

