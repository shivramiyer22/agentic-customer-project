"""
Pydantic schemas for upload endpoints
"""

from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class UploadFileStatus(BaseModel):
    """Status of an individual uploaded file"""
    
    file_name: str = Field(..., description="Name of the uploaded file")
    file_size: int = Field(..., description="Size of the file in bytes")
    status: Literal["queued", "processing", "completed", "failed"] = Field(
        ..., description="Upload status"
    )
    progress: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Upload progress percentage"
    )
    error: Optional[str] = Field(None, description="Error message if upload failed")
    target_collection: Optional[str] = Field(
        None, description="Target ChromaDB collection"
    )
    chunks_count: Optional[int] = Field(
        None, description="Number of chunks created"
    )


class UploadRequest(BaseModel):
    """Upload request schema (for documentation)"""
    
    files: List[str] = Field(
        ..., description="List of file names (handled as multipart/form-data)"
    )
    target_collection: Optional[str] = Field(
        None, description="Target knowledge base collection or 'auto-map'"
    )


class UploadResponse(BaseModel):
    """Upload response schema"""
    
    upload_id: str = Field(..., description="Unique upload ID")
    status: Literal["queued", "processing", "completed", "failed"] = Field(
        ..., description="Overall upload status"
    )
    files: List[UploadFileStatus] = Field(
        ..., description="Status of each uploaded file"
    )
    overall_progress: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Overall progress percentage"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Upload creation timestamp"
    )
    message: Optional[str] = Field(None, description="Optional status message")


class UploadStatusResponse(BaseModel):
    """Upload status response schema"""
    
    upload_id: str = Field(..., description="Upload ID")
    status: Literal["queued", "processing", "completed", "failed"] = Field(
        ..., description="Overall upload status"
    )
    files: List[UploadFileStatus] = Field(
        ..., description="Status of each uploaded file"
    )
    overall_progress: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Overall progress percentage"
    )
    created_at: datetime = Field(..., description="Upload creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

