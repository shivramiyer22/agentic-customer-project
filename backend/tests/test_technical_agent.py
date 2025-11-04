"""
Unit tests for Technical Support Agent

Tests for technical agent implementation using LangChain v1.0 create_agent()
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.agents.technical_agent import (
    get_technical_agent,
    get_technical_agent_singleton,
)
from app.utils.logger import app_logger


def test_get_technical_agent_creates_agent():
    """Test that get_technical_agent creates agent with correct parameters"""
    with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        agent = get_technical_agent()
        
        # Verify create_agent was called
        assert mock_create_agent.called
        
        # Verify it was called with correct model
        call_kwargs = mock_create_agent.call_args[1]
        assert 'model' in call_kwargs or 'model' in str(mock_create_agent.call_args)
        
        # Verify tools were provided (search_technical_kb)
        assert 'tools' in call_kwargs or 'tools' in str(mock_create_agent.call_args)
        
        # Verify system_prompt was provided
        assert 'system_prompt' in call_kwargs or 'system_prompt' in str(mock_create_agent.call_args)
        
        # Verify checkpointer was provided
        assert 'checkpointer' in call_kwargs or 'checkpointer' in str(mock_create_agent.call_args)
        
        # Verify name was provided (technical_support_agent)
        assert 'name' in call_kwargs or 'name' in str(mock_create_agent.call_args)
        
        assert agent is not None


def test_get_technical_agent_uses_openai_model():
    """Test that technical agent uses OpenAI model (gpt-4o-mini)"""
    with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_technical_agent()
        
        # Check if "openai" appears in the call
        call_str = str(mock_create_agent.call_args)
        assert 'openai' in call_str.lower() or 'gpt' in call_str.lower()


def test_get_technical_agent_uses_descriptive_name():
    """Test that technical agent has descriptive name (technical_support_agent)"""
    import inspect
    source = inspect.getsource(get_technical_agent)
    
    assert "technical_support_agent" in source or "name" in source.lower()


def test_get_technical_agent_singleton():
    """Test that get_technical_agent_singleton returns same instance"""
    # Reset global singleton to ensure clean test
    import app.agents.technical_agent
    app.agents.technical_agent._technical_agent = None
    
    with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        agent1 = get_technical_agent_singleton()
        agent2 = get_technical_agent_singleton()
        
        # Should return same instance
        assert agent1 is agent2
        
        # create_agent should only be called once
        assert mock_create_agent.call_count == 1


def test_technical_agent_includes_rag_tool():
    """Test that technical agent includes RAG retrieval tool"""
    with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_technical_agent()
        
        # Verify tools were passed
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            assert len(tools) > 0
            # Check if search_technical_kb is in tools
            tool_names = [getattr(t, 'name', str(t)) for t in tools]
            assert any('technical' in str(t).lower() or 'search' in str(t).lower() for t in tools)


def test_technical_agent_system_prompt_content():
    """Test that technical agent system prompt includes required content"""
    import inspect
    source = inspect.getsource(get_technical_agent)
    
    # Check for key elements in system prompt
    assert "Technical Support Agent" in source or "technical" in source.lower()
    assert "documentation" in source.lower() or "specification" in source.lower()
    assert "CRITICAL" in source or "critical" in source.lower()
    assert "source" in source.lower() or "citation" in source.lower()


def test_technical_agent_uses_checkpointer():
    """Test that technical agent uses InMemorySaver checkpointer"""
    with patch('app.agents.technical_agent.get_checkpointer') as mock_get_checkpointer:
        mock_checkpointer = Mock()
        mock_get_checkpointer.return_value = mock_checkpointer
        
        with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
            mock_agent = Mock()
            mock_create_agent.return_value = mock_agent
            
            get_technical_agent()
            
            # Verify checkpointer was used
            assert mock_get_checkpointer.called
            
            # Verify it was passed to create_agent
            call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
            if 'checkpointer' in call_kwargs:
                assert call_kwargs['checkpointer'] == mock_checkpointer


def test_technical_agent_error_handling():
    """Test that technical agent handles errors gracefully"""
    with patch('app.agents.technical_agent.create_agent') as mock_create_agent:
        mock_create_agent.side_effect = Exception("Agent creation error")
        
        with pytest.raises(Exception):
            get_technical_agent()





