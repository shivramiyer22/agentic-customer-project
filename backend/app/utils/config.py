"""
Configuration utilities and environment variable management
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    OPENAI_EMBEDDING_DIMENSIONS: int = int(os.getenv("OPENAI_EMBEDDING_DIMENSIONS", "1536"))
    
    # AWS Bedrock Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_BEDROCK_MODEL: str = os.getenv("AWS_BEDROCK_MODEL", "bedrock:claude-3-haiku")
    
    # ChromaDB Configuration
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    
    # Application Configuration
    ESCALATION_EMAIL: str = os.getenv("ESCALATION_EMAIL", "john.doe@aerospace-co.com")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # LangSmith Configuration (Optional)
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGSMITH_API_KEY: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "aerospace-customer-service")
    
    # Knowledge Base Collections
    COLLECTION_BILLING: str = "billing_knowledge_base"
    COLLECTION_TECHNICAL: str = "technical_knowledge_base"
    COLLECTION_POLICY: str = "policy_knowledge_base"
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        
        if cls.LANGSMITH_TRACING and not cls.LANGSMITH_API_KEY:
            errors.append("LANGSMITH_API_KEY is required when LANGSMITH_TRACING is enabled")
        
        return errors
    
    @classmethod
    def get_all_collections(cls) -> list[str]:
        """Get list of all knowledge base collection names"""
        return [
            cls.COLLECTION_BILLING,
            cls.COLLECTION_TECHNICAL,
            cls.COLLECTION_POLICY,
        ]


# Global config instance
config = Config()

