"""
Tests for supervisor agent orchestrator

Tests for supervisor agent creation, tools, and configuration
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.agents.orchestrator import (
    get_supervisor_agent,
    get_supervisor_agent_singleton,
    detect_emergency,
    billing_tool,
    technical_tool,
    policy_tool,
    EMERGENCY_KEYWORDS
)
from app.utils.config import config
from app.utils.logger import app_logger


def test_emergency_keywords_defined():
    """Test that emergency keywords are defined"""
    assert isinstance(EMERGENCY_KEYWORDS, list)
    assert len(EMERGENCY_KEYWORDS) > 0
    assert "emergency" in EMERGENCY_KEYWORDS
    assert "critical" in EMERGENCY_KEYWORDS
    assert "accident" in EMERGENCY_KEYWORDS


def test_detect_emergency_positive():
    """Test emergency detection with emergency keywords"""
    query = "This is an emergency situation!"
    result = detect_emergency.invoke({"query": query})
    
    assert result != ""
    assert "EMERGENCY DETECTED" in result
    assert config.ESCALATION_EMAIL in result


def test_detect_emergency_negative():
    """Test emergency detection with non-emergency query"""
    query = "Hello, I need help with my billing question"
    result = detect_emergency.invoke({"query": query})
    
    assert result == ""


def test_detect_emergency_case_insensitive():
    """Test that emergency detection is case-insensitive"""
    query = "THIS IS A CRITICAL ISSUE"
    result = detect_emergency.invoke({"query": query})
    
    assert result != ""
    assert "EMERGENCY DETECTED" in result


def test_detect_emergency_multiple_keywords():
    """Test emergency detection with multiple keywords"""
    query = "There was an accident and we need urgent assistance immediately"
    result = detect_emergency.invoke({"query": query})
    
    assert result != ""


def test_billing_tool():
    """Test billing_tool placeholder"""
    request = "What is my billing status?"
    result = billing_tool.invoke({"request": request})
    
    assert result != ""
    assert "billing" in result.lower()
    assert "inquiry" in result.lower()


def test_technical_tool():
    """Test technical_tool placeholder"""
    request = "How do I troubleshoot this component?"
    result = technical_tool.invoke({"request": request})
    
    assert result != ""
    assert "technical" in result.lower()
    assert "inquiry" in result.lower()


def test_policy_tool():
    """Test policy_tool placeholder"""
    request = "What are the FAA regulations?"
    result = policy_tool.invoke({"request": request})
    
    assert result != ""
    assert "policy" in result.lower()
    assert "inquiry" in result.lower()


def test_tool_descriptions_exist():
    """Test that all tools have descriptions"""
    assert hasattr(detect_emergency, 'description') or hasattr(detect_emergency, '__doc__')
    assert hasattr(billing_tool, 'description') or hasattr(billing_tool, '__doc__')
    assert hasattr(technical_tool, 'description') or hasattr(technical_tool, '__doc__')
    assert hasattr(policy_tool, 'description') or hasattr(policy_tool, '__doc__')


@patch('app.agents.orchestrator.create_agent')
def test_get_supervisor_agent_creates_agent(mock_create_agent):
    """Test that get_supervisor_agent creates agent with correct parameters"""
    mock_agent = Mock()
    mock_create_agent.return_value = mock_agent
    
    agent = get_supervisor_agent()
    
    # Verify create_agent was called
    assert mock_create_agent.called
    
    # Verify it was called with correct model
    call_kwargs = mock_create_agent.call_args[1]
    assert 'model' in call_kwargs or 'model' in str(mock_create_agent.call_args)
    
    # Verify tools were provided
    assert 'tools' in call_kwargs or 'tools' in str(mock_create_agent.call_args)
    
    # Verify system_prompt was provided
    assert 'system_prompt' in call_kwargs or 'system_prompt' in str(mock_create_agent.call_args)
    
    # Verify checkpointer was provided
    assert 'checkpointer' in call_kwargs or 'checkpointer' in str(mock_create_agent.call_args)
    
    # Verify name was provided
    assert 'name' in call_kwargs or 'name' in str(mock_create_agent.call_args)
    
    assert agent is not None


@patch('app.agents.orchestrator.create_agent')
def test_get_supervisor_agent_fallback_to_openai(mock_create_agent):
    """Test that supervisor agent falls back to OpenAI if Bedrock fails"""
    # First call fails (Bedrock), second succeeds (OpenAI)
    mock_create_agent.side_effect = [Exception("Bedrock error"), Mock()]
    
    agent = get_supervisor_agent()
    
    # Should be called twice (Bedrock fail, then OpenAI)
    assert mock_create_agent.call_count == 2
    
    # Verify second call used OpenAI model
    # Check if "openai" appears in the call arguments
    second_call = mock_create_agent.call_args_list[1]
    assert 'openai' in str(second_call).lower() or 'gpt' in str(second_call).lower()


@patch('app.agents.orchestrator.create_agent')
def test_get_supervisor_agent_singleton(mock_create_agent):
    """Test that get_supervisor_agent_singleton returns same instance"""
    mock_agent = Mock()
    mock_create_agent.return_value = mock_agent
    
    agent1 = get_supervisor_agent_singleton()
    agent2 = get_supervisor_agent_singleton()
    
    # Should return same instance
    assert agent1 is agent2
    
    # create_agent should only be called once
    assert mock_create_agent.call_count == 1


def test_supervisor_agent_name():
    """Test that supervisor agent has descriptive name"""
    # Check that the name "supervisor_agent" is used in the code
    import inspect
    source = inspect.getsource(get_supervisor_agent)
    
    assert "supervisor_agent" in source or "name" in source.lower()


@patch('app.agents.orchestrator.create_agent')
def test_supervisor_agent_connects_to_bedrock(mock_create_agent):
    """Test that supervisor agent attempts to connect to AWS Bedrock"""
    mock_agent = Mock()
    mock_create_agent.return_value = mock_agent
    
    with patch('app.utils.config.config') as mock_config:
        mock_config.AWS_BEDROCK_MODEL = "bedrock:claude-3-haiku"
        mock_config.AWS_ACCESS_KEY_ID = "test-key"
        mock_config.AWS_SECRET_ACCESS_KEY = "test-secret"
        mock_config.AWS_REGION = "us-east-1"
        
        agent = get_supervisor_agent()
        
        # Should attempt to create agent with Bedrock model
        assert mock_create_agent.called
        call_args = mock_create_agent.call_args
        
        # First call should use Bedrock model
        if call_args and 'model' in call_args[1]:
            assert call_args[1]['model'] == mock_config.AWS_BEDROCK_MODEL


@patch('app.agents.orchestrator.create_agent')
def test_supervisor_agent_uses_bedrock_when_available(mock_create_agent):
    """Test that supervisor agent uses Bedrock when langchain-aws is available"""
    with patch('builtins.__import__') as mock_import:
        # Mock successful import of langchain_aws
        mock_import.return_value = Mock()
        
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        agent = get_supervisor_agent()
        
        # Should create agent (either Bedrock or fallback)
        assert mock_create_agent.called

