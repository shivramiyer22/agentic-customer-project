"""
Collections endpoint router
"""

from fastapi import APIRouter
from app.retrieval.chroma_client import get_chroma_client
from app.utils.config import config

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/")
async def get_collections():
    """
    Get list of available knowledge base collections
    
    Returns:
        List of available collection names
    """
    try:
        client = get_chroma_client()
        
        # Get configured collections
        configured_collections = config.get_all_collections()
        
        # Get actual collections from ChromaDB
        actual_collections = client.list_collections()
        
        # Combine and deduplicate
        all_collections = list(set(configured_collections + actual_collections))
        
        return {
            "collections": all_collections,
            "configured": configured_collections,
            "count": len(all_collections),
        }
        
    except Exception as e:
        # Return configured collections as fallback
        return {
            "collections": config.get_all_collections(),
            "configured": config.get_all_collections(),
            "count": len(config.get_all_collections()),
            "error": str(e),
        }

