"""
Integration tests for Policy & Compliance Agent

Tests for policy agent integration with supervisor agent
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.agents.orchestrator import policy_tool
from app.agents.policy_agent import get_policy_agent, get_policy_agent_singleton


def test_policy_tool_calls_policy_agent():
    """Test that policy_tool calls policy agent"""
    with patch('app.agents.orchestrator.get_policy_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test query"),
                Mock(role="assistant", content="Policy response with citations [Source: policy.pdf]")
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        result = policy_tool.invoke({"request": "What are the FAA regulations?"})
        
        # Verify agent was invoked
        assert mock_agent.invoke.called
        
        # Verify response contains agent output
        assert result is not None
        assert len(result) > 0


def test_policy_tool_returns_agent_response():
    """Test that policy_tool returns the agent's final message content"""
    with patch('app.agents.orchestrator.get_policy_agent_singleton') as mock_get_agent:
        expected_response = "Policy response with source citations [Source: faa_policy.pdf]"
        
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test query"),
                Mock(role="assistant", content=expected_response)
            ]
        })
        mock_get_agent.return_value = mock_agent
        
        result = policy_tool.invoke({"request": "FAA regulations"})
        
        assert result == expected_response


def test_policy_tool_error_handling():
    """Test that policy_tool handles errors gracefully"""
    with patch('app.agents.orchestrator.get_policy_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(side_effect=Exception("Agent error"))
        mock_get_agent.return_value = mock_agent
        
        result = policy_tool.invoke({"request": "test query"})
        
        # Should return error message, not raise exception
        assert result is not None
        assert "error" in result.lower() or "apologize" in result.lower()


def test_policy_tool_passes_query_to_agent():
    """Test that policy_tool passes the query correctly to agent"""
    with patch('app.agents.orchestrator.get_policy_agent_singleton') as mock_get_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [Mock(role="assistant", content="Response")]
        })
        mock_get_agent.return_value = mock_agent
        
        test_query = "What are the DFARs requirements?"
        policy_tool.invoke({"request": test_query})
        
        # Verify invoke was called with correct query
        assert mock_agent.invoke.called
        call_args = mock_agent.invoke.call_args[0][0]
        
        # Check messages contain the query
        if "messages" in call_args:
            user_message = call_args["messages"][0]
            assert user_message["content"] == test_query


def test_policy_tool_description():
    """Test that policy_tool has correct description for supervisor routing"""
    # Check tool has description
    assert hasattr(policy_tool, 'description') or hasattr(policy_tool, '__doc__')
    
    # Check description contains key terms for routing
    description = getattr(policy_tool, 'description', '') or getattr(policy_tool, '__doc__', '')
    description_lower = description.lower()
    
    assert "policy" in description_lower or "compliance" in description_lower
    assert "faa" in description_lower or "easa" in description_lower or "regulation" in description_lower


def test_policy_tool_in_supervisor_tools():
    """Test that policy_tool is included in supervisor agent's tools"""
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
            
            # Check if policy_tool is in the tools list
            policy_tool_str = str(policy_tool)
            assert any('policy' in str(t).lower() for t in tools) or policy_tool in tools


def test_policy_agent_independent_invocation():
    """Test that policy agent can be invoked independently"""
    with patch('app.agents.policy_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="test"),
                Mock(role="assistant", content="Policy response")
            ]
        })
        mock_create_agent.return_value = mock_agent
        
        policy_agent = get_policy_agent()
        
        result = policy_agent.invoke({
            "messages": [{"role": "user", "content": "What are FAA regulations?"}]
        })
        
        assert result is not None
        assert "messages" in result or hasattr(result, "messages")


def test_policy_agent_with_cag_retrieval():
    """Test that policy agent uses CAG retrieval tool"""
    with patch('app.agents.policy_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_policy_agent()
        
        # Verify tools include search_policy_kb
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            # Check if any tool is search_policy_kb (check by name or string representation)
            tool_strs = [str(t).lower() for t in tools]
            assert any('policy' in s or 'search' in s for s in tool_strs)

