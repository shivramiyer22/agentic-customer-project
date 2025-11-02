"""
Upload endpoint router for document ingestion

Handles multipart file uploads, validates files, and queues ingestion tasks
"""

import os
import uuid
import asyncio
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from app.ingestion.ingest_data import ingest_document, validate_file
from app.ingestion.parsers.parser_factory import get_parser
from app.retrieval.chroma_client import get_chroma_client
from app.utils.config import config
from app.utils.logger import app_logger
from app.schemas.upload import (
    UploadResponse,
    UploadStatusResponse,
    UploadFileStatus,
)


router = APIRouter(prefix="/upload", tags=["upload"])

# In-memory upload status tracking (for MVP - in production, use Redis or database)
upload_status: dict[str, dict] = {}


def save_uploaded_file(file: UploadFile, upload_dir: str = "./uploads") -> Path:
    """
    Save uploaded file to temporary directory
    
    Args:
        file: Uploaded file object
        upload_dir: Directory to save files
        
    Returns:
        Path to saved file
    """
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = Path(upload_dir) / file.filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    return file_path


async def process_upload_task(
    upload_id: str,
    file_path: Path,
    file_name: str,
    file_size: int,
    target_collection: Optional[str],
):
    """
    Background task to process file upload and ingestion
    
    Args:
        upload_id: Upload ID
        file_path: Path to uploaded file
        file_name: Original file name
        file_size: File size in bytes
        target_collection: Target collection or None for auto-map
    """
    try:
        # Update status to processing
        if upload_id in upload_status:
            upload_status[upload_id]["files"][file_name]["status"] = "processing"
            upload_status[upload_id]["files"][file_name]["progress"] = 25.0
            upload_status[upload_id]["status"] = "processing"
            upload_status[upload_id]["updated_at"] = datetime.utcnow()
        
        # Determine if auto-map
        auto_map = target_collection is None or target_collection == "auto-map"
        
        # Ingest document
        result = ingest_document(
            file_path=file_path,
            target_collection=target_collection if not auto_map else None,
            auto_map=auto_map,
        )
        
        # Update status to completed
        if upload_id in upload_status:
            upload_status[upload_id]["files"][file_name]["status"] = "completed"
            upload_status[upload_id]["files"][file_name]["progress"] = 100.0
            upload_status[upload_id]["files"][file_name]["target_collection"] = result["target_collection"]
            upload_status[upload_id]["files"][file_name]["chunks_count"] = result["chunks_count"]
            upload_status[upload_id]["updated_at"] = datetime.utcnow()
            
            # Update overall progress
            all_files = upload_status[upload_id]["files"]
            completed_files = sum(1 for f in all_files.values() if f["status"] == "completed")
            total_files = len(all_files)
            overall_progress = (completed_files / total_files) * 100 if total_files > 0 else 0
            upload_status[upload_id]["overall_progress"] = overall_progress
            
            # Check if all files are completed
            if all(f["status"] in ["completed", "failed"] for f in all_files.values()):
                if any(f["status"] == "failed" for f in all_files.values()):
                    upload_status[upload_id]["status"] = "failed"
                else:
                    upload_status[upload_id]["status"] = "completed"
        
        # Clean up temporary file
        try:
            file_path.unlink()
        except Exception as e:
            app_logger.warning(f"Failed to delete temporary file {file_path}: {e}")
        
        app_logger.info(f"Successfully processed upload {upload_id} file {file_name}")
        
    except Exception as e:
        app_logger.error(f"Error processing upload {upload_id} file {file_name}: {e}")
        
        # Update status to failed
        if upload_id in upload_status:
            upload_status[upload_id]["files"][file_name]["status"] = "failed"
            upload_status[upload_id]["files"][file_name]["error"] = str(e)
            upload_status[upload_id]["files"][file_name]["progress"] = 0.0
            upload_status[upload_id]["updated_at"] = datetime.utcnow()
            
            # Update overall status
            all_files = upload_status[upload_id]["files"]
            if all(f["status"] in ["completed", "failed"] for f in all_files.values()):
                upload_status[upload_id]["status"] = "failed"
        
        # Clean up temporary file
        try:
            file_path.unlink()
        except Exception:
            pass


@router.post("/", response_model=UploadResponse)
async def upload_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(..., description="Files to upload"),
    target_collection: Optional[str] = Form(
        None,
        description="Target knowledge base collection or 'auto-map' (default: auto-map)",
    ),
):
    """
    Upload documents to knowledge base
    
    Accepts multipart file uploads, validates files, and queues ingestion tasks asynchronously
    """
    try:
        # Generate upload ID
        upload_id = str(uuid.uuid4())
        
        # Normalize target_collection
        if target_collection == "auto-map" or target_collection == "":
            target_collection = None
        
        # Validate target collection if provided
        if target_collection and target_collection not in config.get_all_collections():
            raise HTTPException(
                status_code=400,
                detail=f"Invalid target collection: {target_collection}. "
                f"Valid collections: {config.get_all_collections()}",
            )
        
        # Initialize upload status
        upload_status[upload_id] = {
            "upload_id": upload_id,
            "status": "queued",
            "files": {},
            "overall_progress": 0.0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        # Validate and save files
        saved_files = []
        for file in files:
            # Get file size
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            # Save file first (for validation)
            saved_file_path = save_uploaded_file(file)
            
            # Validate file (now that it's saved)
            is_valid, error = validate_file(saved_file_path)
            if not is_valid:
                upload_status[upload_id]["files"][file.filename] = {
                    "file_name": file.filename,
                    "file_size": file_size,
                    "status": "failed",
                    "progress": 0.0,
                    "error": error,
                }
                # Clean up invalid file
                try:
                    saved_file_path.unlink()
                except Exception:
                    pass
                continue
            
            saved_files.append((saved_file_path, file.filename, file_size))
            
            # Initialize file status
            upload_status[upload_id]["files"][file.filename] = {
                "file_name": file.filename,
                "file_size": file_size,
                "status": "queued",
                "progress": 0.0,
                "error": None,
                "target_collection": None,
                "chunks_count": None,
            }
        
        # Check if any files were successfully saved
        if not saved_files:
            raise HTTPException(
                status_code=400,
                detail="No valid files to upload",
            )
        
        # Queue background tasks for each file
        for saved_file_path, file_name, file_size in saved_files:
            background_tasks.add_task(
                process_upload_task,
                upload_id,
                saved_file_path,
                file_name,
                file_size,
                target_collection,
            )
        
        # Convert files status to response format
        files_status = [
            UploadFileStatus(**file_data)
            for file_data in upload_status[upload_id]["files"].values()
        ]
        
        response = UploadResponse(
            upload_id=upload_id,
            status="queued",
            files=files_status,
            overall_progress=0.0,
            created_at=upload_status[upload_id]["created_at"],
        )
        
        app_logger.info(
            f"Queued upload {upload_id} with {len(saved_files)} files "
            f"(target_collection: {target_collection or 'auto-map'})"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in upload endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/status/{upload_id}", response_model=UploadStatusResponse)
async def get_upload_status(upload_id: str):
    """
    Get upload status by upload ID
    
    Args:
        upload_id: Upload ID
        
    Returns:
        Upload status response
    """
    if upload_id not in upload_status:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    status_data = upload_status[upload_id]
    
    # Convert files status to response format
    files_status = [
        UploadFileStatus(**file_data)
        for file_data in status_data["files"].values()
    ]
    
    response = UploadStatusResponse(
        upload_id=status_data["upload_id"],
        status=status_data["status"],
        files=files_status,
        overall_progress=status_data["overall_progress"],
        created_at=status_data["created_at"],
        updated_at=status_data["updated_at"],
    )
    
    return response

