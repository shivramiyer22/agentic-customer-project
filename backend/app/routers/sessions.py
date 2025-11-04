"""
Sessions endpoint router for managing chat sessions
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.utils.logger import app_logger

router = APIRouter(prefix="/sessions", tags=["sessions"])


# In-memory session store (for MVP)
# In production, this should be replaced with a database
sessions_store: dict[str, dict] = {}


class SessionCreate(BaseModel):
    """Session creation request model"""
    session_id: Optional[str] = None


class Session(BaseModel):
    """Session response model"""
    session_id: str
    created_at: str
    updated_at: str
    message_count: int = 0
    agent: Optional[str] = None


@router.get("/")
async def get_sessions() -> dict:
    """
    Get list of all chat sessions
    
    Returns:
        List of all sessions
    """
    try:
        sessions = []
        for session_id, session_data in sessions_store.items():
            sessions.append(Session(
                session_id=session_id,
                created_at=session_data.get("created_at", datetime.utcnow().isoformat()),
                updated_at=session_data.get("updated_at", datetime.utcnow().isoformat()),
                message_count=session_data.get("message_count", 0),
                agent=session_data.get("agent"),
            ))
        
        # Sort by updated_at descending (most recent first)
        sessions.sort(key=lambda x: x.updated_at, reverse=True)
        
        return {
            "sessions": [s.dict() for s in sessions],
            "count": len(sessions),
        }
    except Exception as e:
        app_logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}")
async def get_session(session_id: str) -> dict:
    """
    Get a specific session by ID
    
    Args:
        session_id: The session identifier
        
    Returns:
        Session details
    """
    try:
        if session_id not in sessions_store:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions_store[session_id]
        
        return Session(
            session_id=session_id,
            created_at=session_data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=session_data.get("updated_at", datetime.utcnow().isoformat()),
            message_count=session_data.get("message_count", 0),
            agent=session_data.get("agent"),
        ).dict()
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error getting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_session(session: Optional[SessionCreate] = None) -> dict:
    """
    Create a new chat session
    
    Args:
        session: Optional session creation data
        
    Returns:
        Created session details
    """
    try:
        import uuid
        
        # Generate session ID if not provided
        session_id = session.session_id if session and session.session_id else f"session-{uuid.uuid4().hex[:12]}"
        
        now = datetime.utcnow().isoformat()
        
        # Create session in store
        sessions_store[session_id] = {
            "created_at": now,
            "updated_at": now,
            "message_count": 0,
            "agent": None,
        }
        
        app_logger.info(f"Created new session: {session_id}")
        
        return Session(
            session_id=session_id,
            created_at=now,
            updated_at=now,
            message_count=0,
            agent=None,
        ).dict()
        
    except Exception as e:
        app_logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def delete_session(session_id: str) -> dict:
    """
    Delete a session
    
    Args:
        session_id: The session identifier to delete
        
    Returns:
        Success message
    """
    try:
        if session_id not in sessions_store:
            raise HTTPException(status_code=404, detail="Session not found")
        
        del sessions_store[session_id]
        app_logger.info(f"Deleted session: {session_id}")
        
        return {
            "message": "Session deleted successfully",
            "session_id": session_id,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error deleting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))






