"""
ChromaDB client initialization and collection management

LangChain Version: v1.0+
Documentation Reference: https://docs.langchain.com/oss/python/langchain/vector-stores/chroma
Last Verified: November 2025
"""

import os
from typing import Optional, Dict, Any, List
from chromadb import PersistentClient
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.utils.config import config
from app.utils.logger import app_logger


class ChromaDBClient:
    """ChromaDB client wrapper for managing vector database"""
    
    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize ChromaDB client with local persistence
        
        Args:
            persist_directory: Directory path for persistent storage
                              (default: from config)
        """
        self.persist_directory = persist_directory or config.CHROMA_DB_PATH
        
        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB persistent client
        self.client = PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model=config.OPENAI_EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
            dimensions=config.OPENAI_EMBEDDING_DIMENSIONS,
        )
        
        # Dictionary to store collection instances
        self._collections: Dict[str, Chroma] = {}
        
        app_logger.info(
            f"ChromaDB client initialized with persist_directory: {self.persist_directory}"
        )
    
    def get_or_create_collection(
        self,
        collection_name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Chroma:
        """
        Get or create a ChromaDB collection
        
        Args:
            collection_name: Name of the collection
            metadata: Optional metadata for the collection
            
        Returns:
            Chroma vector store instance
        """
        if collection_name in self._collections:
            return self._collections[collection_name]
        
        try:
            # Create or get collection using LangChain Chroma
            # ChromaDB requires non-empty metadata, so provide default if empty
            collection_metadata = metadata if metadata else {"type": "knowledge_base"}
            
            vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
                client=self.client,
                collection_metadata=collection_metadata,
            )
            
            self._collections[collection_name] = vectorstore
            
            app_logger.info(f"Collection '{collection_name}' ready")
            
            return vectorstore
            
        except Exception as e:
            app_logger.error(f"Error creating collection '{collection_name}': {e}")
            raise
    
    def get_collection(self, collection_name: str) -> Optional[Chroma]:
        """
        Get an existing collection
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Chroma vector store instance or None if not found
        """
        if collection_name in self._collections:
            return self._collections[collection_name]
        
        try:
            # Try to get existing collection
            vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
                client=self.client,
            )
            
            self._collections[collection_name] = vectorstore
            return vectorstore
            
        except Exception as e:
            app_logger.warning(f"Collection '{collection_name}' not found: {e}")
            return None
    
    def list_collections(self) -> List[str]:
        """
        List all available collections
        
        Returns:
            List of collection names
        """
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            app_logger.error(f"Error listing collections: {e}")
            return []
    
    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection
        
        Args:
            collection_name: Name of the collection to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if collection_name in self._collections:
                del self._collections[collection_name]
            
            self.client.delete_collection(name=collection_name)
            app_logger.info(f"Collection '{collection_name}' deleted")
            return True
            
        except Exception as e:
            app_logger.error(f"Error deleting collection '{collection_name}': {e}")
            return False
    
    def reset(self) -> bool:
        """
        Reset the ChromaDB client (delete all collections)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.reset()
            self._collections.clear()
            app_logger.info("ChromaDB client reset")
            return True
            
        except Exception as e:
            app_logger.error(f"Error resetting ChromaDB client: {e}")
            return False


# Global ChromaDB client instance
_chroma_client: Optional[ChromaDBClient] = None


def get_chroma_client() -> ChromaDBClient:
    """
    Get or create global ChromaDB client instance
    
    Returns:
        ChromaDBClient instance
    """
    global _chroma_client
    
    if _chroma_client is None:
        _chroma_client = ChromaDBClient()
    
    return _chroma_client


def initialize_knowledge_bases():
    """
    Initialize all three knowledge base collections
    
    Returns:
        Dictionary mapping collection names to Chroma instances
    """
    client = get_chroma_client()
    
    collections = {}
    
    for collection_name in config.get_all_collections():
        collections[collection_name] = client.get_or_create_collection(
            collection_name=collection_name,
            metadata={
                "description": f"Knowledge base collection: {collection_name}",
                "created_by": "aerospace_customer_service",
                "type": "knowledge_base",
            },
        )
    
    app_logger.info(f"Initialized {len(collections)} knowledge base collections")
    
    return collections


# Alias for backward compatibility
initialize_collections = initialize_knowledge_bases

