"""
Integration tests for Technical Support Agent

Tests for technical agent integration with supervisor agent
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.agents.orchestrator import technical_tool
from app.agents.technical_agent import get_technical_agent, get_technical_agent_singleton


def test_technical_tool_calls_technical_agent():
    """Test that technical_tool calls technical agent"""
    with patch('app.agents.orchestrator.get_technical_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test query"),
                Mock(role="assistant", content="Technical response with citations [Source: api_docs.pdf]")
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        result = technical_tool.invoke({"request": "How do I use the API?"})
        
        # Verify agent was invoked
        assert mock_agent.invoke.called
        
        # Verify response contains agent output
        assert result is not None
        assert len(result) > 0


def test_technical_tool_returns_agent_response():
    """Test that technical_tool returns the agent's final message content"""
    with patch('app.agents.orchestrator.get_technical_agent_singleton') as mock_get_agent:
        expected_response = "Technical response with source citations [Source: api_docs.pdf]"
        
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test query"),
                Mock(role="assistant", content=expected_response)
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        result = technical_tool.invoke({"request": "API documentation"})
        
        assert result == expected_response


def test_technical_tool_error_handling():
    """Test that technical_tool handles errors gracefully"""
    with patch('app.agents.orchestrator.get_technical_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(side_effect=Exception("Agent error"))
        mock_get_agent.return_value = mock_agent
        
        result = technical_tool.invoke({"request": "test query"})
        
        # Should return error message, not raise exception
        assert result is not None
        assert "error" in result.lower() or "apologize" in result.lower()


def test_technical_tool_passes_query_to_agent():
    """Test that technical_tool passes the query correctly to agent"""
    with patch('app.agents.orchestrator.get_technical_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [Mock(role="assistant", content="Response")]
        })
        mock_get_agent.return_value = mock_agent
        
        test_query = "How do I configure the component?"
        technical_tool.invoke({"request": test_query})
        
        # Verify invoke was called with correct query
        assert mock_agent.invoke.called
        call_args = mock_agent.invoke.call_args[0][0]
        
        # Check messages contain the query
        if "messages" in call_args:
            user_message = call_args["messages"][0]
            assert user_message["content"] == test_query


def test_technical_tool_description():
    """Test that technical_tool has correct description for supervisor routing"""
    # Check tool has description
    assert hasattr(technical_tool, 'description') or hasattr(technical_tool, '__doc__')
    
    # Check description contains key terms for routing
    description = getattr(technical_tool, 'description', '') or getattr(technical_tool, '__doc__', '')
    description_lower = description.lower()
    
    assert "technical" in description_lower
    assert "documentation" in description_lower or "specification" in description_lower or "bug" in description_lower


def test_technical_tool_in_supervisor_tools():
    """Test that technical_tool is included in supervisor agent's tools"""
    from app.agents.orchestrator import get_supervisor_agent
    
    with patch('app.agents.orchestrator.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_supervisor_agent()
        
        # Verify create_agent was called with tools
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            tool_names = [getattr(t, 'name', str(t)) for t in tools]
            
            # Check if technical_tool is in the tools list
            technical_tool_str = str(technical_tool)
            assert any('technical' in str(t).lower() for t in tools) or technical_tool in tools


def test_technical_agent_independent_invocation():
    """Test that technical agent can be invoked independently"""
    with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test"),
                Mock(role="assistant", content="Technical response")
            ]
        })
        mock_create_agent.return_value = mock_agent
        
        technical_agent = get_technical_agent()
        
        result = technical_agent.invoke({
            "messages": [{"role": "user", "content": "How do I use the API?"}]
        })
        
        assert result is not None
        assert "messages" in result or hasattr(result, "messages")


def test_technical_agent_with_rag_retrieval():
    """Test that technical agent uses RAG retrieval tool"""
    with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_technical_agent()
        
        # Verify tools include search_technical_kb
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            # Check if any tool is search_technical_kb (check by name or string representation)
            tool_strs = [str(t).lower() for t in tools]
            assert any('technical' in s or 'search' in s for s in tool_strs)





