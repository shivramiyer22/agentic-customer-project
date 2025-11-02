"""
Pydantic schemas for chat endpoints

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/messages
Last Verified: November 2025
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message request model"""
    
    session_id: Optional[str] = Field(None, description="Session identifier for conversation continuity (generated if not provided)")
    message: str = Field(..., description="User message content")
    stream: Optional[bool] = Field(False, description="Whether to stream response as SSE")


class ChatResponse(BaseModel):
    """Chat response model (non-streaming)"""
    
    session_id: str = Field(..., description="Session identifier")
    message: str = Field(..., description="Agent response content")
    agent: str = Field(..., description="Name of the agent that handled the request")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Source citations")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ChatStreamChunk(BaseModel):
    """SSE stream chunk model"""
    
    content: Optional[str] = Field(None, description="Streaming token content")
    agent: Optional[str] = Field(None, description="Agent name")
    done: Optional[bool] = Field(None, description="Whether stream is complete")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

