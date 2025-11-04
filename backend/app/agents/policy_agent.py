"""
Policy & Compliance Agent implementation using LangChain v1.0

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: November 2025

This module implements the Policy & Compliance Agent using Pure CAG retrieval strategy.
"""

from typing import Optional
from langchain.agents import create_agent
from app.retrieval.cag_retriever import search_policy_kb
from app.state.conversation_state import get_checkpointer
from app.utils.config import config
from app.utils.logger import app_logger


def get_policy_agent():
    """
    Create or get Policy & Compliance Agent instance
    
    Returns:
        Policy & Compliance Agent configured with CAG retrieval tool
    """
    checkpointer = get_checkpointer()
    
    # Policy agent system prompt emphasizing domain expertise and critical instructions
    policy_prompt = (
        "You are the Policy & Compliance Agent for The Aerospace Company Customer Service system. "
        "You specialize in regulatory compliance, FAA/EASA regulations, DFARs policies, "
        "data governance, and customer support policies.\n\n"
        
        "Your Responsibilities:\n"
        "- Provide accurate information about regulatory compliance requirements\n"
        "- Answer questions about FAA/EASA regulations\n"
        "- Explain DFARs (Defense Federal Acquisition Regulation Supplement) policies\n"
        "- Provide guidance on data governance policies\n"
        "- Answer questions about customer support policies, terms of service, and privacy policies\n"
        "- Ensure all responses comply with legal and regulatory requirements\n\n"
        
        "CRITICAL INSTRUCTIONS:\n"
        "- **ALWAYS** use the search_policy_kb tool to retrieve relevant policy documents before answering\n"
        "- **ALWAYS** include ALL results, findings, and details in your final response\n"
        "- **ALWAYS** cite your sources using the document names and excerpts provided by search_policy_kb\n"
        "- The supervisor agent only sees your final message - include everything in that message\n"
        "- Be precise, concise without redundancies, and accurate - policy information must be correct\n"
        "- If you don't find relevant information, clearly state that and suggest contacting compliance@aerospace-co.com\n\n"
        
        "Response Format:\n"
        "- Start with a clear answer to the question\n"
        "- Include relevant policy excerpts and citations\n"
        "- Reference specific regulations or policy documents when applicable\n"
        "- End with source citations in the format: [Source: document_name]\n\n"
        
        "Important:\n"
        "- Never guess or make up policy information\n"
        "- If information is not found in the knowledge base, say so clearly\n"
        "- Always verify information comes from search_policy_kb tool results"
    )
    
    try:
        # Create policy agent using create_agent() from langchain.agents
        policy_agent = create_agent(
            model="openai:gpt-4o-mini",  # OpenAI model as specified
            tools=[search_policy_kb],
            system_prompt=policy_prompt,
            checkpointer=checkpointer,
            name="policy_compliance_agent"  # Descriptive name as required
        )
        
        app_logger.info("Policy & Compliance Agent created successfully")
        return policy_agent
        
    except Exception as e:
        app_logger.error(f"Error creating policy agent: {e}")
        raise


# Global policy agent instance
_policy_agent: Optional[object] = None


def get_policy_agent_singleton():
    """
    Get or create singleton Policy & Compliance Agent instance
    
    Returns:
        Policy & Compliance Agent instance (singleton pattern)
    """
    global _policy_agent
    
    if _policy_agent is None:
        _policy_agent = get_policy_agent()
    
    return _policy_agent





