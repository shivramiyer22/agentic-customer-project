"""
Technical Support Agent implementation using LangChain v1.0

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/agents
Last Verified: November 2025

This module implements the Technical Support Agent using Pure RAG retrieval strategy.
"""

from typing import Optional
from langchain.agents import create_agent
from app.retrieval.rag_retriever import search_technical_kb
from app.state.conversation_state import get_checkpointer
from app.utils.config import config
from app.utils.logger import app_logger


def get_technical_agent():
    """
    Create or get Technical Support Agent instance
    
    Returns:
        Technical Support Agent configured with RAG retrieval tool
    """
    checkpointer = get_checkpointer()
    
    # Technical agent system prompt emphasizing domain expertise and critical instructions
    technical_prompt = (
        "You are the Technical Support Agent for The Aerospace Company Customer Service system. "
        "You specialize in technical documentation, bug reports, component specifications, "
        "troubleshooting guides, and engineering questions.\n\n"
        
        "Your Responsibilities:\n"
        "- Provide accurate technical information from documentation and knowledge base\n"
        "- Answer questions about component specifications and technical details\n"
        "- Help troubleshoot technical issues based on bug reports and documentation\n"
        "- Explain technical concepts and system architecture\n"
        "- Guide users through technical procedures and workflows\n"
        "- Provide solutions based on technical manuals and specifications\n\n"
        
        "CRITICAL INSTRUCTIONS:\n"
        "- **ALWAYS** use the search_technical_kb tool to retrieve relevant technical documents before answering\n"
        "- **ALWAYS** include ALL results, findings, and details in your final response\n"
        "- **ALWAYS** cite your sources using the document names and excerpts provided by search_technical_kb\n"
        "- The supervisor agent only sees your final message - include everything in that message\n"
        "- Be precise and technical - provide accurate information from documentation\n"
        "- If you don't find relevant information, clearly state that and suggest contacting technical@aerospace-co.com\n\n"
        
        "Response Format:\n"
        "- Start with a clear answer to the technical question\n"
        "- Include relevant technical excerpts and citations from documentation\n"
        "- Reference specific documents, sections, or specifications when applicable\n"
        "- Provide step-by-step instructions when troubleshooting\n"
        "- End with source citations in the format: [Source: document_name]\n\n"
        
        "Important:\n"
        "- Never guess or make up technical information\n"
        "- If information is not found in the knowledge base, say so clearly\n"
        "- Always verify information comes from search_technical_kb tool results\n"
        "- Focus on technical accuracy and clarity"
    )
    
    try:
        # Create technical agent using create_agent() from langchain.agents
        technical_agent = create_agent(
            model="openai:gpt-4o-mini",  # OpenAI model as specified
            tools=[search_technical_kb],
            system_prompt=technical_prompt,
            checkpointer=checkpointer,
            name="technical_support_agent"  # Descriptive name as required
        )
        
        app_logger.info("Technical Support Agent created successfully")
        return technical_agent
        
    except Exception as e:
        app_logger.error(f"Error creating technical agent: {e}")
        raise


# Global technical agent instance
_technical_agent: Optional[object] = None


def get_technical_agent_singleton():
    """
    Get or create singleton Technical Support Agent instance
    
    Returns:
        Technical Support Agent instance (singleton pattern)
    """
    global _technical_agent
    
    if _technical_agent is None:
        _technical_agent = get_technical_agent()
    
    return _technical_agent





