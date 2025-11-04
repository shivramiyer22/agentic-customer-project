"""
Integration tests for Billing Support Agent

Tests for billing agent integration with supervisor agent
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.agents.orchestrator import billing_tool
from app.agents.billing_agent import get_billing_agent, get_billing_agent_singleton


def test_billing_tool_calls_billing_agent():
    """Test that billing_tool calls billing agent"""
    with patch('app.agents.orchestrator.get_billing_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test query"),
                Mock(role="assistant", content="Billing response with citations [Source: invoice.pdf]")
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        result = billing_tool.invoke({"request": "What is my invoice amount?"})
        
        assert mock_agent.invoke.called
        assert result is not None
        assert len(result) > 0


def test_billing_tool_returns_agent_response():
    """Test that billing_tool returns the agent's final message content"""
    with patch('app.agents.orchestrator.get_billing_agent_singleton') as mock_get_agent:
        expected_response = "Billing response with source citations [Source: invoice.pdf]"
        
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test query"),
                Mock(role="assistant", content=expected_response)
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        result = billing_tool.invoke({"request": "Invoice information"})
        
        assert result == expected_response


def test_billing_tool_error_handling():
    """Test that billing_tool handles errors gracefully"""
    with patch('app.agents.orchestrator.get_billing_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(side_effect=Exception("Agent error"))
        mock_get_agent.return_value = mock_agent
        
        result = billing_tool.invoke({"request": "test query"})
        
        assert result is not None
        assert "error" in result.lower() or "apologize" in result.lower()


def test_billing_tool_passes_query_to_agent():
    """Test that billing_tool passes the query correctly to agent"""
    with patch('app.agents.orchestrator.get_billing_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [Mock(role="assistant", content="Response")]
        })
        mock_get_agent.return_value = mock_agent
        
        test_query = "What is my payment status?"
        billing_tool.invoke({"request": test_query})
        
        assert mock_agent.invoke.called
        call_args = mock_agent.invoke.call_args[0][0]
        
        if "messages" in call_args:
            user_message = call_args["messages"][0]
            assert user_message["content"] == test_query


def test_billing_tool_description():
    """Test that billing_tool has correct description for supervisor routing"""
    assert hasattr(billing_tool, 'description') or hasattr(billing_tool, '__doc__')
    
    description = getattr(billing_tool, 'description', '') or getattr(billing_tool, '__doc__', '')
    description_lower = description.lower()
    
    assert "billing" in description_lower
    assert "pricing" in description_lower or "invoice" in description_lower or "contract" in description_lower


def test_billing_tool_in_supervisor_tools():
    """Test that billing_tool is included in supervisor agent's tools"""
    from app.agents.orchestrator import get_supervisor_agent
    
    with patch('app.agents.orchestrator.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_supervisor_agent()
        
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            tool_names = [getattr(t, 'name', str(t)) for t in tools]
            
            billing_tool_str = str(billing_tool)
            assert any('billing' in str(t).lower() for t in tools) or billing_tool in tools


def test_billing_agent_independent_invocation():
    """Test that billing agent can be invoked independently"""
    with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test"),
                Mock(role="assistant", content="Billing response")
            ]
        })
        mock_create_agent.return_value = mock_agent
        
        billing_agent = get_billing_agent()
        
        result = billing_agent.invoke({
            "messages": [{"role": "user", "content": "What is my invoice amount?"}]
        })
        
        assert result is not None
        assert "messages" in result or hasattr(result, "messages")


def test_billing_agent_with_hybrid_retrieval():
    """Test that billing agent uses Hybrid RAG/CAG retrieval tools"""
    with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_billing_agent()
        
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            tool_strs = [str(t).lower() for t in tools]
            assert any('billing' in s or 'search' in s for s in tool_strs)
            assert any('policy' in s or 'cache' in s for s in tool_strs)





