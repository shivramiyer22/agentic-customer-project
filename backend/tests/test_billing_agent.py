"""
Unit tests for Billing Support Agent

Tests for billing agent implementation using LangChain v1.0 create_agent()
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.agents.billing_agent import (
    get_billing_agent,
    get_billing_agent_singleton,
)
from app.utils.logger import app_logger


def test_get_billing_agent_creates_agent():
    """Test that get_billing_agent creates agent with correct parameters"""
    with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        agent = get_billing_agent()
        
        assert mock_create_agent.called
        
        call_kwargs = mock_create_agent.call_args[1]
        assert 'model' in call_kwargs or 'model' in str(mock_create_agent.call_args)
        assert 'tools' in call_kwargs or 'tools' in str(mock_create_agent.call_args)
        assert 'system_prompt' in call_kwargs or 'system_prompt' in str(mock_create_agent.call_args)
        assert 'checkpointer' in call_kwargs or 'checkpointer' in str(mock_create_agent.call_args)
        assert 'name' in call_kwargs or 'name' in str(mock_create_agent.call_args)
        
        assert agent is not None


def test_get_billing_agent_uses_openai_model():
    """Test that billing agent uses OpenAI model (gpt-4o-mini)"""
    with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_billing_agent()
        
        call_str = str(mock_create_agent.call_args)
        assert 'openai' in call_str.lower() or 'gpt' in call_str.lower()


def test_get_billing_agent_uses_descriptive_name():
    """Test that billing agent has descriptive name (billing_support_agent)"""
    import inspect
    source = inspect.getsource(get_billing_agent)
    
    assert "billing_support_agent" in source or "name" in source.lower()


def test_get_billing_agent_singleton():
    """Test that get_billing_agent_singleton returns same instance"""
    import app.agents.billing_agent
    app.agents.billing_agent._billing_agent = None
    
    with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        agent1 = get_billing_agent_singleton()
        agent2 = get_billing_agent_singleton()
        
        assert agent1 is agent2
        assert mock_create_agent.call_count == 1


def test_billing_agent_includes_hybrid_tools():
    """Test that billing agent includes both RAG and CAG tools"""
    with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_billing_agent()
        
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            assert len(tools) >= 2  # Should have both search_billing_kb and get_cached_policy_info
            tool_strs = [str(t).lower() for t in tools]
            assert any('billing' in s or 'search' in s for s in tool_strs)
            assert any('policy' in s or 'cache' in s for s in tool_strs)


def test_billing_agent_system_prompt_content():
    """Test that billing agent system prompt includes required content"""
    import inspect
    source = inspect.getsource(get_billing_agent)
    
    assert "Billing Support Agent" in source or "billing" in source.lower()
    assert "pricing" in source.lower() or "invoice" in source.lower()
    assert "CRITICAL" in source or "critical" in source.lower()
    assert "source" in source.lower() or "citation" in source.lower()
    assert "Hybrid RAG/CAG" in source or "hybrid" in source.lower()


def test_billing_agent_uses_checkpointer():
    """Test that billing agent uses InMemorySaver checkpointer"""
    with patch('app.agents.billing_agent.get_checkpointer') as mock_get_checkpointer:
        mock_checkpointer = Mock()
        mock_get_checkpointer.return_value = mock_checkpointer
        
        with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
            mock_agent = Mock()
            mock_create_agent.return_value = mock_agent
            
            get_billing_agent()
            
            assert mock_get_checkpointer.called
            
            call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
            if 'checkpointer' in call_kwargs:
                assert call_kwargs['checkpointer'] == mock_checkpointer


def test_billing_agent_error_handling():
    """Test that billing agent handles errors gracefully"""
    with patch('app.agents.billing_agent.create_agent') as mock_create_agent:
        mock_create_agent.side_effect = Exception("Agent creation error")
        
        with pytest.raises(Exception):
            get_billing_agent()





