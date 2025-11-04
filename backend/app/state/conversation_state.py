"""
Conversation state management with InMemorySaver for conversation persistence

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/short-term-memory
Last Verified: November 2025
"""

from typing import Optional
from langgraph.checkpoint.memory import InMemorySaver
from app.utils.logger import app_logger


# Global checkpointer instance
_checkpointer: Optional[InMemorySaver] = None


def get_checkpointer() -> InMemorySaver:
    """
    Get or create global InMemorySaver checkpointer instance
    
    Returns:
        InMemorySaver instance for conversation persistence
    """
    global _checkpointer
    
    if _checkpointer is None:
        _checkpointer = InMemorySaver()
        app_logger.info("InMemorySaver checkpointer initialized for conversation persistence")
    
    return _checkpointer





