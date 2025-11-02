"""
Supervisor Agent (Orchestrator) implementation using LangChain v1.0

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: November 2025

This module implements the supervisor agent using the tool calling pattern,
where the supervisor routes queries to specialized worker agents as tools.
"""

from typing import Optional
from langchain.agents import create_agent
from langchain_core.tools import tool
from app.state.conversation_state import get_checkpointer
from app.agents.policy_agent import get_policy_agent_singleton
from app.agents.technical_agent import get_technical_agent_singleton
from app.agents.billing_agent import get_billing_agent_singleton
from app.utils.config import config
from app.utils.logger import app_logger


# Emergency keywords for safety-critical detection
EMERGENCY_KEYWORDS = [
    "emergency", "critical", "urgent", "immediate", "safety", "hazard",
    "accident", "incident", "failure", "malfunction", "explosion", "fire",
    "injury", "fatal", "casualty", "evacuation", "mayday", "distress",
    "grounded", "grounded aircraft", "grounding", "aircraft down",
    "system failure", "engine failure", "structural failure"
]


@tool
def detect_emergency(query: str) -> str:
    """
    Analyze query for safety-critical keywords and detect emergencies.
    Returns escalation message with contact information if emergency detected.
    
    Args:
        query: User query to analyze
        
    Returns:
        Escalation message if emergency detected, empty string otherwise
    """
    query_lower = query.lower()
    
    # Check for emergency keywords
    emergency_found = any(keyword in query_lower for keyword in EMERGENCY_KEYWORDS)
    
    if emergency_found:
        escalation_message = (
            f"⚠️ EMERGENCY DETECTED ⚠️\n\n"
            f"Safety-critical issue detected in your query. "
            f"Please contact our emergency escalation team immediately:\n\n"
            f"Email: {config.ESCALATION_EMAIL}\n\n"
            f"Your query has been flagged for immediate human review. "
            f"Please do not rely solely on this AI system for emergency situations."
        )
        app_logger.warning(f"Emergency detected in query: {query[:100]}")
        return escalation_message
    
    return ""


@tool
def billing_tool(request: str) -> str:
    """
    Handle billing inquiries, pricing questions, contract terms, and invoices.
    Use this tool for questions about billing, pricing, contracts, invoices, payment plans,
    subscription changes, refunds, or billing-related account issues.

    Args:
        request: User query about billing, pricing, contracts, or invoices

    Returns:
        Response from billing support agent with billing information and source citations
    """
    try:
        app_logger.info(f"Billing tool called with request: {request[:100]}")

        # Get billing agent instance
        billing_agent = get_billing_agent_singleton()

        # Invoke billing agent with the query
        # Note: We don't pass session_id here because each tool call gets a fresh context
        # The supervisor manages the overall conversation state
        result = billing_agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })

        # Extract final message content from agent response
        if "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            response_content = final_message.content if hasattr(final_message, "content") else str(final_message)
        else:
            response_content = str(result)

        app_logger.info(f"Billing agent response generated (length: {len(response_content)})")

        return response_content

    except Exception as e:
        app_logger.error(f"Error invoking billing agent: {e}")
        return (
            f"I apologize, but I encountered an error processing your billing inquiry: {str(e)}. "
            "Please try again or contact billing@aerospace-co.com for assistance."
        )


@tool
def technical_tool(request: str) -> str:
    """
    Handle technical questions, component specifications, bug reports, and technical manuals.
    Use this tool for questions about technical documentation, component specifications,
    bug reports, troubleshooting, technical support, engineering questions, or system documentation.

    Args:
        request: User query about technical issues, documentation, or specifications

    Returns:
        Response from technical support agent with technical information and source citations
    """
    try:
        app_logger.info(f"Technical tool called with request: {request[:100]}")

        # Get technical agent instance
        technical_agent = get_technical_agent_singleton()

        # Invoke technical agent with the query
        # Note: We don't pass session_id here because each tool call gets a fresh context
        # The supervisor manages the overall conversation state
        result = technical_agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })

        # Extract final message content from agent response
        if "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            response_content = final_message.content if hasattr(final_message, "content") else str(final_message)
        else:
            response_content = str(result)

        app_logger.info(f"Technical agent response generated (length: {len(response_content)})")

        return response_content

    except Exception as e:
        app_logger.error(f"Error invoking technical agent: {e}")
        return (
            f"I apologize, but I encountered an error processing your technical inquiry: {str(e)}. "
            "Please try again or contact technical@aerospace-co.com for assistance."
        )


@tool
def policy_tool(request: str) -> str:
    """
    Handle regulatory compliance questions, FAA/EASA regulations, and policy inquiries.
    Use this tool for questions about regulatory compliance, FAA/EASA regulations, DFARs policies,
    data governance, customer support policies, terms of service, privacy policies, or legal compliance.
    
    Args:
        request: User query about policies, regulations, or compliance
        
    Returns:
        Response from policy & compliance agent with policy information and source citations
    """
    try:
        app_logger.info(f"Policy tool called with request: {request[:100]}")
        
        # Get policy agent instance
        policy_agent = get_policy_agent_singleton()
        
        # Invoke policy agent with the query
        # Note: We don't pass session_id here because each tool call gets a fresh context
        # The supervisor manages the overall conversation state
        result = policy_agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })
        
        # Extract final message content from agent response
        if "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            response_content = final_message.content if hasattr(final_message, "content") else str(final_message)
        else:
            response_content = str(result)
        
        app_logger.info(f"Policy agent response generated (length: {len(response_content)})")
        
        return response_content
        
    except Exception as e:
        app_logger.error(f"Error invoking policy agent: {e}")
        return (
            f"I apologize, but I encountered an error processing your policy inquiry: {str(e)}. "
            "Please try again or contact compliance@aerospace-co.com for assistance."
        )


def get_supervisor_agent():
    """
    Create or get supervisor agent instance
    
    Returns:
        Supervisor agent configured with worker tools and emergency detection
    """
    checkpointer = get_checkpointer()
    
    # Supervisor system prompt emphasizing query routing
    supervisor_prompt = (
        "You are the supervisor agent for The Aerospace Company Customer Service system. "
        "Your primary responsibility is to analyze incoming customer queries and route them "
        "to the appropriate specialized worker agent using the available tools.\n\n"
        
        "Available Worker Agents:\n"
        "1. **billing_tool**: Use for billing inquiries, pricing questions, contract terms, invoices, "
        "payment plans, refunds, or billing-related account issues.\n"
        "2. **technical_tool**: Use for technical questions, component specifications, bug reports, "
        "technical manuals, troubleshooting, engineering questions, or system documentation.\n"
        "3. **policy_tool**: Use for regulatory compliance questions, FAA/EASA regulations, DFARs policies, "
        "data governance, customer support policies, terms of service, privacy policies, or legal compliance.\n\n"
        
        "Routing Guidelines:\n"
        "- Analyze the query intent carefully before routing with the help of your accessible LLM\n"
        "- If the query contains safety-critical keywords (emergency, critical, urgent, accident, etc.), "
        "use detect_emergency tool FIRST\n"
        "- **IMPORTANT**: If a user query contains multiple distinct questions that require different worker agents, "
        "you MUST call multiple tools to answer all parts of the query. These tool calls can be made in parallel or sequentially as needed.\n"
        "- For example, if asked 'How many bugs were resolved and what is the SLA policy?', "
        "you should call BOTH technical_tool (for bug count) AND policy_tool (for SLA policy)\n"
        "- Route to the most appropriate worker agent(s) based on the question(s) being asked\n"
        "- Each distinct sub-question should be routed to its appropriate specialist agent\n"
        "- Provide clear, helpful responses that incorporate ALL worker agents' outputs\n\n"
        
        "Important:\n"
        "- Always check for emergencies first using detect_emergency\n"
        "- **When a query has multiple parts, call ALL relevant tools - do not choose just one**\n"
        "- Be concise and professional in your responses\n"
        "- Acknowledge the customer's inquiry and provide helpful guidance\n"
        "- Combine responses from multiple worker agents when needed to fully answer the query\n"
        "- If routing to multiple worker agents, synthesize their responses into a coherent answer"
    )
    
    try:
        # Create supervisor agent using create_agent() from langchain.agents
        # Using AWS Bedrock model as specified in requirements
        supervisor = create_agent(
            model=config.AWS_BEDROCK_MODEL,  # "bedrock:claude-3-haiku" or similar
            tools=[detect_emergency, billing_tool, technical_tool, policy_tool],
            system_prompt=supervisor_prompt,
            checkpointer=checkpointer,
            name="supervisor_agent"  # Descriptive name as required
        )
        
        app_logger.info("Supervisor agent created successfully")
        return supervisor
        
    except Exception as e:
        app_logger.error(f"Error creating supervisor agent: {e}")
        # Fallback to OpenAI model if Bedrock is not available
        app_logger.warning("Falling back to OpenAI model for supervisor agent")
        try:
            supervisor = create_agent(
                model="openai:gpt-4o-mini",
                tools=[detect_emergency, billing_tool, technical_tool, policy_tool],
                system_prompt=supervisor_prompt,
                checkpointer=checkpointer,
                name="supervisor_agent"
            )
            app_logger.info("Supervisor agent created with OpenAI fallback")
            return supervisor
        except Exception as fallback_error:
            app_logger.error(f"Error creating supervisor agent with fallback: {fallback_error}")
            raise


# Global supervisor agent instance
_supervisor_agent: Optional[object] = None


def get_supervisor_agent_singleton():
    """
    Get or create singleton supervisor agent instance
    
    Returns:
        Supervisor agent instance (singleton pattern)
    """
    global _supervisor_agent
    
    if _supervisor_agent is None:
        _supervisor_agent = get_supervisor_agent()
    
    return _supervisor_agent


# Type alias for supervisor agent
SupervisorAgent = type(get_supervisor_agent())

