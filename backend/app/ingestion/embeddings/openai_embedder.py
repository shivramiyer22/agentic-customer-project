"""
OpenAI embedding generator using OpenAIEmbeddings

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/integrations/openai_embeddings
Last Verified: November 2025
"""

from typing import List
from langchain_openai import OpenAIEmbeddings  # pyright: ignore[reportMissingImports]
from app.utils.config import config
from app.utils.logger import app_logger


def get_embedder() -> OpenAIEmbeddings:
    """
    Get OpenAI embeddings instance
    
    Returns:
        OpenAIEmbeddings instance
    """
    return OpenAIEmbeddings(
        model=config.OPENAI_EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY,
        dimensions=config.OPENAI_EMBEDDING_DIMENSIONS,
    )


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts
    
    Args:
        texts: List of text strings
        
    Returns:
        List of embedding vectors
    """
    try:
        embedder = get_embedder()
        embeddings = embedder.embed_documents(texts)
        
        app_logger.info(f"Generated {len(embeddings)} embeddings")
        
        return embeddings
        
    except Exception as e:
        app_logger.error(f"Error generating embeddings: {e}")
        raise

