"""
Agent implementations for the aerospace customer service system

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: November 2025
"""

from app.agents.orchestrator import get_supervisor_agent, SupervisorAgent
from app.agents.policy_agent import get_policy_agent, get_policy_agent_singleton
from app.agents.technical_agent import get_technical_agent, get_technical_agent_singleton
from app.agents.billing_agent import get_billing_agent, get_billing_agent_singleton

__all__ = [
    "get_supervisor_agent",
    "SupervisorAgent",
    "get_policy_agent",
    "get_policy_agent_singleton",
    "get_technical_agent",
    "get_technical_agent_singleton",
    "get_billing_agent",
    "get_billing_agent_singleton",
]

