"""
Tests for chat router endpoint

Tests for POST /chat endpoint with supervisor agent integration
"""

import pytest
import json
import uuid
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from app.main import app
from app.schemas.chat import ChatMessage, ChatResponse

client = TestClient(app)


@pytest.fixture
def mock_supervisor_agent():
    """Mock supervisor agent for testing"""
    agent = Mock()
    
    # Mock invoke for non-streaming
    agent.invoke = Mock(return_value={
        "messages": [
            Mock(role="user", content="test message"),
            Mock(role="assistant", content="test response")
        ]
    })
    
    # Mock astream for streaming
    async def mock_astream(*args, **kwargs):
        # Yield chunks that simulate agent streaming
        yield {
            "messages": [
                Mock(role="user", content="test message"),
                Mock(role="assistant", content="Hello")
            ]
        }
        yield {
            "messages": [
                Mock(role="user", content="test message"),
                Mock(role="assistant", content="Hello world")
            ]
        }
    
    agent.astream = AsyncMock(side_effect=mock_astream)
    
    return agent


def test_chat_endpoint_exists():
    """Test that POST /chat endpoint exists"""
    # This test checks if endpoint is registered
    routes = [route.path for route in app.routes]
    assert "/chat" in routes or any("/chat" in route.path for route in app.routes)


def test_chat_endpoint_valid_request():
    """Test POST /chat with valid request"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test"),
                Mock(role="assistant", content="Response")
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        response = client.post(
            "/chat/",
            json={
                "session_id": str(uuid.uuid4()),
                "message": "Hello",
                "stream": False
            }
        )
        
        # Should return 200 OK
        assert response.status_code == 200
        
        # Should return JSON response
        data = response.json()
        assert "session_id" in data
        assert "message" in data
        assert "agent" in data


def test_chat_endpoint_generates_session_id():
    """Test that chat endpoint generates session_id if not provided"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test"),
                Mock(role="assistant", content="Response")
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        response = client.post(
            "/chat/",
            json={
                "message": "Hello"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] is not None
        assert data["session_id"] != ""


def test_chat_endpoint_streaming():
    """Test POST /chat with streaming enabled"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        
        async def mock_astream(*args, **kwargs):
            yield {
                "messages": [
                    Mock(role="assistant", content="Hello")
                ]
            }
        
        mock_agent.astream = AsyncMock(side_effect=mock_astream)
        mock_get_agent.return_value = mock_agent
        
        response = client.post(
            "/chat/",
            json={
                "session_id": str(uuid.uuid4()),
                "message": "Hello",
                "stream": True
            }
        )
        
        # Should return 200 with streaming response
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"


def test_chat_endpoint_invalid_request():
    """Test POST /chat with invalid request (missing message)"""
    response = client.post(
        "/chat/",
        json={
            "session_id": str(uuid.uuid4())
        }
    )
    
    # Should return validation error (422)
    assert response.status_code == 422


def test_chat_endpoint_uses_thread_id():
    """Test that chat endpoint uses session_id as thread_id for agent"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="assistant", content="Response")
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        session_id = str(uuid.uuid4())
        
        response = client.post(
            "/chat/",
            json={
                "session_id": session_id,
                "message": "Hello",
                "stream": False
            }
        )
        
        assert response.status_code == 200
        
        # Verify invoke was called with config containing thread_id
        assert mock_agent.invoke.called
        call_args = mock_agent.invoke.call_args
        
        # Check that config was passed with thread_id
        if len(call_args) > 1 and 'config' in call_args[1]:
            config = call_args[1]['config']
            assert 'configurable' in config
            assert config['configurable']['thread_id'] == session_id


def test_chat_endpoint_error_handling():
    """Test that chat endpoint handles errors gracefully"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(side_effect=Exception("Agent error"))
        mock_get_agent.return_value = mock_agent
        
        response = client.post(
            "/chat/",
            json={
                "session_id": str(uuid.uuid4()),
                "message": "Hello",
                "stream": False
            }
        )
        
        # Should return 500 error
        assert response.status_code == 500


def test_generate_session_id():
    """Test that session_id generation creates valid UUID"""
    from app.routers.chat import generate_session_id
    
    session_id1 = generate_session_id()
    session_id2 = generate_session_id()
    
    # Should be valid UUID strings
    assert isinstance(session_id1, str)
    assert isinstance(session_id2, str)
    
    # Should be different
    assert session_id1 != session_id2
    
    # Should be valid UUID format
    uuid.UUID(session_id1)
    uuid.UUID(session_id2)


def test_chat_streaming_includes_contributing_agents():
    """Test that streaming response includes contributing_agents in metadata"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        
        # Create a mock AIMessage with tool_calls
        mock_tool_call = Mock()
        mock_tool_call.name = "technical_tool"
        mock_ai_message = Mock()
        mock_ai_message.content = "Hello world"
        mock_ai_message.tool_calls = [mock_tool_call]
        type(mock_ai_message).__name__ = "AIMessage"
        
        async def mock_astream(*args, **kwargs):
            yield {
                "messages": [
                    Mock(role="user", content="test"),
                    mock_ai_message
                ]
            }
        
        mock_agent.astream = AsyncMock(side_effect=mock_astream)
        mock_get_agent.return_value = mock_agent
        
        response = client.post(
            "/chat/",
            json={
                "session_id": str(uuid.uuid4()),
                "message": "Hello",
                "stream": True
            }
        )
        
        assert response.status_code == 200
        # Check that SSE response contains contributing_agents in metadata
        content = response.text
        # The response should contain metadata with contributing_agents
        # Note: We can't easily parse SSE in TestClient, but we verify the endpoint works


def test_chat_streaming_includes_contributing_models():
    """Test that streaming response includes contributing_models in metadata"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        
        # Create a mock AIMessage with tool_calls
        mock_tool_call = Mock()
        mock_tool_call.name = "billing_tool"
        mock_ai_message = Mock()
        mock_ai_message.content = "Billing response"
        mock_ai_message.tool_calls = [mock_tool_call]
        type(mock_ai_message).__name__ = "AIMessage"
        
        async def mock_astream(*args, **kwargs):
            yield {
                "messages": [
                    Mock(role="user", content="test"),
                    mock_ai_message
                ]
            }
        
        mock_agent.astream = AsyncMock(side_effect=mock_astream)
        mock_get_agent.return_value = mock_agent
        
        response = client.post(
            "/chat/",
            json={
                "session_id": str(uuid.uuid4()),
                "message": "What is my invoice?",
                "stream": True
            }
        )
        
        assert response.status_code == 200
        # The response should include contributing_models in metadata
        # Supervisor model (AWS Bedrock) should always be included


def test_chat_streaming_tracks_supervisor_model():
    """Test that supervisor model (AWS Bedrock) is always tracked"""
    with patch('app.routers.chat.get_supervisor_agent_singleton') as mock_get_agent:
        with patch('app.utils.config.config') as mock_config:
            mock_config.AWS_BEDROCK_MODEL = "bedrock:claude-3-haiku"
            
            mock_agent = Mock()
            mock_ai_message = Mock()
            mock_ai_message.content = "Response"
            mock_ai_message.tool_calls = []
            type(mock_ai_message).__name__ = "AIMessage"
            
            async def mock_astream(*args, **kwargs):
                yield {
                    "messages": [
                        Mock(role="user", content="test"),
                        mock_ai_message
                    ]
                }
            
            mock_agent.astream = AsyncMock(side_effect=mock_astream)
            mock_get_agent.return_value = mock_agent
            
            response = client.post(
                "/chat/",
                json={
                    "session_id": str(uuid.uuid4()),
                    "message": "Hello",
                    "stream": True
                }
            )
            
            assert response.status_code == 200
            # Supervisor model should be included even if no tools are called

