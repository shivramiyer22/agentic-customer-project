"""
Health endpoint router
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.retrieval.chroma_client import get_chroma_client
from app.utils.logger import app_logger

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """
    Health check endpoint that verifies ChromaDB connectivity
    
    Returns:
        Health status with ChromaDB connection status
    """
    try:
        # Check ChromaDB connectivity
        client = get_chroma_client()
        collections = client.list_collections()
        
        return {
            "status": "healthy",
            "chromadb": {
                "connected": True,
                "collections_count": len(collections),
                "collections": collections,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        app_logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "chromadb": {
                    "connected": False,
                    "error": str(e),
                },
            }
        )

