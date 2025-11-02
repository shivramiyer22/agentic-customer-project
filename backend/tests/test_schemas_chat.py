"""
Tests for chat schemas

Tests for ChatMessage, ChatResponse, and ChatStreamChunk Pydantic models
"""

import pytest
from pydantic import ValidationError
from app.schemas.chat import ChatMessage, ChatResponse, ChatStreamChunk


def test_chat_message_valid():
    """Test valid ChatMessage creation"""
    message = ChatMessage(
        session_id="test-session-123",
        message="Hello, I need help",
        stream=True
    )
    
    assert message.session_id == "test-session-123"
    assert message.message == "Hello, I need help"
    assert message.stream is True


def test_chat_message_default_stream():
    """Test ChatMessage with default stream=False"""
    message = ChatMessage(
        session_id="test-session-123",
        message="Hello"
    )
    
    assert message.stream is False


def test_chat_message_required_fields():
    """Test that ChatMessage requires message (session_id is optional)"""
    # session_id is optional, so this should not raise
    message1 = ChatMessage(session_id="test", message="test")
    assert message1.session_id == "test"
    assert message1.message == "test"
    
    # message is required, so this should raise
    with pytest.raises(ValidationError):
        ChatMessage(session_id="test")
    
    # session_id is optional, so this should not raise
    message2 = ChatMessage(message="test")
    assert message2.message == "test"
    assert message2.session_id is None


def test_chat_response_valid():
    """Test valid ChatResponse creation"""
    response = ChatResponse(
        session_id="test-session-123",
        message="Here is your response",
        agent="supervisor_agent",
        sources=[{"source": "test"}],
        metadata={"test": "value"}
    )
    
    assert response.session_id == "test-session-123"
    assert response.message == "Here is your response"
    assert response.agent == "supervisor_agent"
    assert len(response.sources) == 1
    assert response.metadata["test"] == "value"


def test_chat_response_defaults():
    """Test ChatResponse with default values"""
    response = ChatResponse(
        session_id="test-session-123",
        message="Response",
        agent="supervisor_agent"
    )
    
    assert response.sources == []
    assert response.metadata is None


def test_chat_stream_chunk_valid():
    """Test valid ChatStreamChunk creation"""
    chunk = ChatStreamChunk(
        content="Hello",
        agent="supervisor_agent",
        done=False
    )
    
    assert chunk.content == "Hello"
    assert chunk.agent == "supervisor_agent"
    assert chunk.done is False


def test_chat_stream_chunk_all_optional():
    """Test ChatStreamChunk with all optional fields"""
    chunk = ChatStreamChunk()
    
    assert chunk.content is None
    assert chunk.agent is None
    assert chunk.done is None
    assert chunk.metadata is None


def test_chat_stream_chunk_done_signal():
    """Test ChatStreamChunk with done=True"""
    chunk = ChatStreamChunk(
        content="",
        agent="supervisor_agent",
        done=True
    )
    
    assert chunk.done is True

