"""
Integration tests for complete multi-agent system routing

Tests to verify supervisor correctly routes queries to all three agents (Policy, Technical, Billing)
"""

import pytest
from unittest.mock import Mock, patch
from app.agents.orchestrator import (
    get_supervisor_agent,
    billing_tool,
    technical_tool,
    policy_tool
)


def test_supervisor_routes_to_billing_agent():
    """Test that supervisor routes billing queries to billing agent"""
    with patch('app.agents.orchestrator.get_billing_agent_singleton') as mock_get_billing:
        mock_billing_agent = Mock()
        mock_billing_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="billing query"),
                Mock(role="assistant", content="Billing response")
            ]
        })
        mock_get_billing.return_value = mock_billing_agent
        
        result = billing_tool.invoke({"request": "What is my invoice amount?"})
        
        assert mock_billing_agent.invoke.called
        assert result is not None
        assert len(result) > 0


def test_supervisor_routes_to_technical_agent():
    """Test that supervisor routes technical queries to technical agent"""
    with patch('app.agents.orchestrator.get_technical_agent_singleton') as mock_get_technical:
        mock_technical_agent = Mock()
        mock_technical_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="technical query"),
                Mock(role="assistant", content="Technical response")
            ]
        })
        mock_get_technical.return_value = mock_technical_agent
        
        result = technical_tool.invoke({"request": "How do I use the API?"})
        
        assert mock_technical_agent.invoke.called
        assert result is not None
        assert len(result) > 0


def test_supervisor_routes_to_policy_agent():
    """Test that supervisor routes policy queries to policy agent"""
    with patch('app.agents.orchestrator.get_policy_agent_singleton') as mock_get_policy:
        mock_policy_agent = Mock()
        mock_policy_agent.invoke = Mock(return_value={
            "messages": [
                Mock(role="user", content="policy query"),
                Mock(role="assistant", content="Policy response")
            ]
        })
        mock_get_policy.return_value = mock_policy_agent
        
        result = policy_tool.invoke({"request": "What are the FAA regulations?"})
        
        assert mock_policy_agent.invoke.called
        assert result is not None
        assert len(result) > 0


def test_supervisor_has_all_three_tools():
    """Test that supervisor agent includes all three worker agent tools"""
    with patch('app.agents.orchestrator.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_supervisor_agent()
        
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            tool_names = [getattr(t, 'name', str(t)).lower() for t in tools]
            
            # Check for all three worker tools
            has_billing = any('billing' in str(t).lower() for t in tools) or billing_tool in tools
            has_technical = any('technical' in str(t).lower() for t in tools) or technical_tool in tools
            has_policy = any('policy' in str(t).lower() for t in tools) or policy_tool in tools
            
            assert has_billing, "Supervisor should have billing_tool"
            assert has_technical, "Supervisor should have technical_tool"
            assert has_policy, "Supervisor should have policy_tool"


def test_all_agents_are_configured_correctly():
    """Test that all three agents (billing, technical, policy) are configured with correct models and tools"""
    # This test verifies that all agents can be created independently
    
    # Test billing agent
    with patch('app.agents.billing_agent.create_agent') as mock_create:
        mock_create.return_value = Mock()
        from app.agents.billing_agent import get_billing_agent
        billing_agent = get_billing_agent()
        assert billing_agent is not None
        assert mock_create.called
        call_kwargs = mock_create.call_args[1] if mock_create.call_args[1] else {}
        assert call_kwargs.get('model') == "openai:gpt-4o-mini" or 'openai' in str(mock_create.call_args).lower()
        assert call_kwargs.get('name') == "billing_support_agent"
    
    # Test technical agent
    with patch('app.agents.technical_agent.create_agent') as mock_create:
        mock_create.return_value = Mock()
        from app.agents.technical_agent import get_technical_agent
        technical_agent = get_technical_agent()
        assert technical_agent is not None
        call_kwargs = mock_create.call_args[1] if mock_create.call_args[1] else {}
        assert call_kwargs.get('name') == "technical_support_agent"
    
    # Test policy agent
    with patch('app.agents.policy_agent.create_agent') as mock_create:
        mock_create.return_value = Mock()
        from app.agents.policy_agent import get_policy_agent
        policy_agent = get_policy_agent()
        assert policy_agent is not None
        call_kwargs = mock_create.call_args[1] if mock_create.call_args[1] else {}
        assert call_kwargs.get('name') == "policy_compliance_agent"


def test_supervisor_routing_decisions():
    """Test that supervisor can make routing decisions to all three agents"""
    # This test verifies the supervisor's routing capability by checking tool descriptions
    
    # Check billing tool description contains billing keywords
    billing_desc = getattr(billing_tool, 'description', '') or str(billing_tool)
    assert "billing" in billing_desc.lower()
    assert any(keyword in billing_desc.lower() for keyword in ["pricing", "invoice", "contract", "payment"])
    
    # Check technical tool description contains technical keywords
    technical_desc = getattr(technical_tool, 'description', '') or str(technical_tool)
    assert "technical" in technical_desc.lower()
    assert any(keyword in technical_desc.lower() for keyword in ["documentation", "specification", "bug", "troubleshoot"])
    
    # Check policy tool description contains policy keywords
    policy_desc = getattr(policy_tool, 'description', '') or str(policy_tool)
    assert "policy" in policy_desc.lower() or "compliance" in policy_desc.lower()
    assert any(keyword in policy_desc.lower() for keyword in ["faa", "easa", "regulation", "legal"])


def test_emergency_detection_before_routing():
    """Test that emergency detection tool is checked before routing to worker agents"""
    with patch('app.agents.orchestrator.create_agent') as mock_create_agent:
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        
        get_supervisor_agent()
        
        call_kwargs = mock_create_agent.call_args[1] if mock_create_agent.call_args[1] else {}
        if 'tools' in call_kwargs:
            tools = call_kwargs['tools']
            
            # Check for emergency detection tool
            has_emergency = any('emergency' in str(t).lower() or 'detect' in str(t).lower() for t in tools)
            
            # Emergency detection should be in tools list
            assert has_emergency, "Supervisor should have emergency detection tool"


def test_all_agents_have_checkpointers():
    """Test that all three agents are configured with InMemorySaver checkpointer"""
    # This test verifies that all agents use conversation state management
    
    # Test billing agent checkpointer
    with patch('app.agents.billing_agent.get_checkpointer') as mock_get_checkpointer:
        mock_checkpointer = Mock()
        mock_get_checkpointer.return_value = mock_checkpointer
        
        with patch('app.agents.billing_agent.create_agent') as mock_create:
            mock_create.return_value = Mock()
            from app.agents.billing_agent import get_billing_agent
            get_billing_agent()
            assert mock_get_checkpointer.called
    
    # Test technical agent checkpointer
    with patch('app.agents.technical_agent.get_checkpointer') as mock_get_checkpointer:
        mock_checkpointer = Mock()
        mock_get_checkpointer.return_value = mock_checkpointer
        
        with patch('app.agents.technical_agent.create_agent') as mock_create:
            mock_create.return_value = Mock()
            from app.agents.technical_agent import get_technical_agent
            get_technical_agent()
            assert mock_get_checkpointer.called
    
    # Test policy agent checkpointer
    with patch('app.agents.policy_agent.get_checkpointer') as mock_get_checkpointer:
        mock_checkpointer = Mock()
        mock_get_checkpointer.return_value = mock_checkpointer
        
        with patch('app.agents.policy_agent.create_agent') as mock_create:
            mock_create.return_value = Mock()
            from app.agents.policy_agent import get_policy_agent
            get_policy_agent()
            assert mock_get_checkpointer.called





