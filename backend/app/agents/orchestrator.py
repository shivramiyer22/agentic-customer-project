"""
Supervisor Agent (Orchestrator) implementation using LangChain v1.0

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: November 2025

This module implements the supervisor agent using the tool calling pattern,
where the supervisor routes queries to specialized worker agents as tools.
"""

from typing import Optional
from langchain.agents import create_agent  # pyright: ignore[reportMissingImports]
from langchain_core.tools import tool  # pyright: ignore[reportMissingImports]
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
        "You are the Supervisor Agent for The Aerospace Company Customer Service system. "
        "Your primary responsibility is to analyze incoming customer queries and route them "
        "to the appropriate specialized worker agent using the available tools.\n\n"
        
        "**CRITICAL - Self-Identification:**\n"
        "- When users ask who they are connecting with, or ask about your identity, you MUST respond: "
        "'You are connecting with the Supervisor Agent for the Aerospace Company Customer Service system.'\n"
        "- Always refer to yourself as 'Supervisor Agent' (not 'Aerospace Company Customer Service System' or 'customer service system').\n"
        "- When introducing yourself or describing your role, always say 'I am the Supervisor Agent' or 'As the Supervisor Agent'.\n\n"
        
        "Available Worker Agents:\n"
        "1. **billing_tool** (Billing Tool Agent): Use for billing inquiries, pricing questions, contract terms, invoices, "
        "payment plans, refunds, or billing-related account issues.\n"
        "2. **technical_tool** (Technical Tool Agent): Use for technical questions, component specifications, bug reports, "
        "technical manuals, troubleshooting, engineering questions, or system documentation.\n"
        "3. **policy_tool** (Policy Tool Agent): Use for regulatory compliance questions, FAA/EASA regulations, DFARs policies, "
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
        "- If routing to multiple worker agents, synthesize their responses into a coherent answer\n"
        "- **CRITICAL**: When communicating with users, always refer to the specialists by their proper names: "
        "'Billing Tool Agent' (not 'Billing Tool'), 'Technical Tool Agent' (not 'Technical Tool'), "
        "and 'Policy Tool Agent' (not 'Policy Tool'). Use these full names when describing what each specialist can do."
    )
    
    # Try to initialize Bedrock model with bearer token if available
    # Use ONLY AWS_BEARER_TOKEN_BEDROCK - do not use AWS_ACCESS_KEY_ID
    bedrock_model = None
    if config.AWS_BEARER_TOKEN_BEDROCK:
        try:
            from langchain_aws import ChatBedrock  # pyright: ignore[reportMissingImports]
            app_logger.info("Initializing Bedrock model with AWS_BEARER_TOKEN_BEDROCK authentication...")
            
            # Initialize Bedrock model with bearer token ONLY
            # Use AWS_BEARER_TOKEN_BEDROCK as both access_key_id and secret_access_key
            # Do NOT use AWS_ACCESS_KEY_ID when bearer token is available
            bedrock_model = ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                region_name=config.AWS_REGION,
                aws_access_key_id=config.AWS_BEARER_TOKEN_BEDROCK,
                aws_secret_access_key=config.AWS_BEARER_TOKEN_BEDROCK,
                credentials_profile_name=None,
            )
            
            # Test the Bedrock connection by making a simple invoke call
            # This will fail if authentication is invalid, allowing us to fall back to OpenAI
            try:
                app_logger.info("Testing Bedrock connection...")
                test_response = bedrock_model.invoke("test")
                app_logger.info("Bedrock model initialized and connection tested successfully with AWS_BEARER_TOKEN_BEDROCK")
            except Exception as auth_error:
                # Authentication failed - fall back to OpenAI
                app_logger.warning(f"Bedrock authentication failed: {auth_error}")
                app_logger.warning("Falling back to OpenAI model for supervisor agent")
                bedrock_model = None
                
        except ImportError:
            app_logger.warning("langchain-aws not available, falling back to OpenAI")
            bedrock_model = None
        except Exception as e:
            app_logger.warning(f"Failed to initialize Bedrock with AWS_BEARER_TOKEN_BEDROCK: {e}, falling back to OpenAI")
            bedrock_model = None
    
    # Create supervisor agent - use Bedrock if available, otherwise use OpenAI
    try:
        if bedrock_model:
            # Use Bedrock model
            supervisor = create_agent(
                model=bedrock_model,
                tools=[detect_emergency, billing_tool, technical_tool, policy_tool],
                system_prompt=supervisor_prompt,
                checkpointer=checkpointer,
                name="supervisor_agent"
            )
            app_logger.info("Supervisor agent created successfully with AWS Bedrock")
            return supervisor
        else:
            # Fallback to OpenAI model
            app_logger.warning("Using OpenAI model for supervisor agent (Bedrock not available or connection failed)")
            supervisor = create_agent(
                model="openai:gpt-4o-mini",
                tools=[detect_emergency, billing_tool, technical_tool, policy_tool],
                system_prompt=supervisor_prompt,
                checkpointer=checkpointer,
                name="supervisor_agent"
            )
            app_logger.info("Supervisor agent created with OpenAI fallback")
            return supervisor
            
    except Exception as e:
        app_logger.error(f"Error creating supervisor agent: {e}")
        # Final fallback to OpenAI if agent creation fails
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

