"""
Feedback API router for collecting user satisfaction ratings
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import json
import os
from pathlib import Path

from app.utils.logger import app_logger

router = APIRouter(prefix="/feedback", tags=["feedback"])

# Feedback data model
class FeedbackRequest(BaseModel):
    """Request model for user feedback submission"""
    session_id: str = Field(..., description="Session ID for the conversation")
    rating: str = Field(..., description="User rating: 'thumbs_up' or 'thumbs_down'")
    comment: Optional[str] = Field(None, description="Optional user comment")

class FeedbackResponse(BaseModel):
    """Response model for feedback submission"""
    message: str
    feedback_id: str
    timestamp: str


# Simple file-based feedback storage (can be replaced with database later)
FEEDBACK_DIR = Path("backend/feedback_data")
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit user feedback",
    description="Submit user satisfaction feedback for a conversation session"
)
async def submit_feedback(feedback: FeedbackRequest) -> FeedbackResponse:
    """
    Submit user feedback for a conversation session.
    
    Args:
        feedback: FeedbackRequest containing session_id, rating, and optional comment
        
    Returns:
        FeedbackResponse with confirmation message and feedback ID
        
    Raises:
        HTTPException: If feedback submission fails
    """
    try:
        # Validate rating
        if feedback.rating not in ["thumbs_up", "thumbs_down"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be 'thumbs_up' or 'thumbs_down'"
            )
        
        # Generate feedback ID and timestamp
        timestamp = datetime.utcnow().isoformat()
        feedback_id = f"{feedback.session_id}_{timestamp}"
        
        # Store feedback data
        feedback_data = {
            "feedback_id": feedback_id,
            "session_id": feedback.session_id,
            "rating": feedback.rating,
            "comment": feedback.comment,
            "timestamp": timestamp
        }
        
        # Save to file (simple implementation - can be replaced with DB)
        feedback_file = FEEDBACK_DIR / f"{feedback_id}.json"
        with open(feedback_file, "w") as f:
            json.dump(feedback_data, f, indent=2)
        
        app_logger.info(
            f"Feedback submitted: session={feedback.session_id}, "
            f"rating={feedback.rating}, has_comment={feedback.comment is not None}"
        )
        
        return FeedbackResponse(
            message="Feedback submitted successfully",
            feedback_id=feedback_id,
            timestamp=timestamp
        )
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )


@router.get(
    "/{session_id}",
    summary="Get feedback for a session",
    description="Retrieve all feedback submitted for a specific session"
)
async def get_session_feedback(session_id: str):
    """
    Retrieve feedback for a specific session.
    
    Args:
        session_id: The session ID to retrieve feedback for
        
    Returns:
        List of feedback entries for the session
    """
    try:
        feedback_files = list(FEEDBACK_DIR.glob(f"{session_id}_*.json"))
        
        if not feedback_files:
            return {"session_id": session_id, "feedback": []}
        
        feedback_list = []
        for feedback_file in feedback_files:
            with open(feedback_file, "r") as f:
                feedback_list.append(json.load(f))
        
        return {
            "session_id": session_id,
            "feedback": feedback_list,
            "count": len(feedback_list)
        }
        
    except Exception as e:
        app_logger.error(f"Error retrieving feedback for session {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve feedback: {str(e)}"
        )




