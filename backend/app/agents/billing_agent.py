"""
Billing Support Agent implementation using LangChain v1.0

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: November 2025

This module implements the Billing Support Agent using Hybrid RAG/CAG retrieval strategy.
"""

from typing import Optional
from langchain.agents import create_agent
from app.retrieval.hybrid_retriever import search_billing_kb, get_cached_policy_info
from app.state.conversation_state import get_checkpointer
from app.utils.config import config
from app.utils.logger import app_logger


def get_billing_agent():
    """
    Create or get Billing Support Agent instance
    
    Returns:
        Billing Support Agent configured with Hybrid RAG/CAG retrieval tools
    """
    checkpointer = get_checkpointer()
    
    # Billing agent system prompt emphasizing domain expertise and critical instructions
    billing_prompt = (
        "You are the Billing Support Agent for The Aerospace Company Customer Service system. "
        "You specialize in billing inquiries, pricing questions, contract terms, invoices, "
        "payment plans, refunds, and billing-related account issues.\n\n"
        
        "Your Responsibilities:\n"
        "- Provide accurate billing information from documentation and knowledge base\n"
        "- Answer questions about pricing, contracts, and invoices\n"
        "- Help with payment plans and subscription changes\n"
        "- Process refund requests and billing-related account issues\n"
        "- Combine billing-specific information with relevant policy information\n"
        "- Provide solutions based on billing documents and policies\n\n"
        
        "CRITICAL INSTRUCTIONS:\n"
        "- **ALWAYS** use the search_billing_kb tool to retrieve relevant billing documents before answering\n"
        "- **ALWAYS** use the get_cached_policy_info tool when billing questions relate to policies, regulations, or compliance\n"
        "- **ALWAYS** include ALL results, findings, and details in your final response\n"
        "- **ALWAYS** cite your sources using the document names and excerpts provided by the tools\n"
        "- The supervisor agent only sees your final message - include everything in that message\n"
        "- Be precise, concise without redundancies, and accurate - billing information must be correct\n"
        "- If you don't find relevant information, clearly state that and suggest contacting billing@aerospace-co.com\n\n"
        
        "Hybrid RAG/CAG Strategy:\n"
        "- Use search_billing_kb for billing-specific queries (pricing, invoices, contracts)\n"
        "- Use get_cached_policy_info for policy-related queries (regulations, compliance)\n"
        "- The get_cached_policy_info tool will cache policy information in session memory\n"
        "- Subsequent queries in the same session will use cached policy data when applicable\n"
        "- Combine both billing and policy information when answering queries that span both domains\n\n"
        
        "Response Format:\n"
        "- Start with a clear answer to the billing question\n"
        "- Include relevant billing excerpts and citations from search_billing_kb\n"
        "- Include relevant policy excerpts and citations from get_cached_policy_info when applicable\n"
        "- Reference specific documents, contracts, or policies when applicable\n"
        "- End with source citations in the format: [Source: document_name]\n\n"
        
        "Important:\n"
        "- Never guess or make up billing information\n"
        "- If information is not found in the knowledge base, say so clearly\n"
        "- Always verify information comes from tool results\n"
        "- Use cached policy data when appropriate to improve response speed"
    )
    
    try:
        # Create billing agent using create_agent() from langchain.agents
        # Include both RAG and CAG tools for Hybrid RAG/CAG strategy
        billing_agent = create_agent(
            model="openai:gpt-4o-mini",  # OpenAI model as specified
            tools=[search_billing_kb, get_cached_policy_info],  # Both RAG and CAG tools
            system_prompt=billing_prompt,
            checkpointer=checkpointer,
            name="billing_support_agent"  # Descriptive name as required
        )
        
        app_logger.info("Billing Support Agent created successfully")
        return billing_agent
        
    except Exception as e:
        app_logger.error(f"Error creating billing agent: {e}")
        raise


# Global billing agent instance
_billing_agent: Optional[object] = None


def get_billing_agent_singleton():
    """
    Get or create singleton Billing Support Agent instance
    
    Returns:
        Billing Support Agent instance (singleton pattern)
    """
    global _billing_agent
    
    if _billing_agent is None:
        _billing_agent = get_billing_agent()
    
    return _billing_agent





