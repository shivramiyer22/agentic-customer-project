"""
FastAPI application entry point with CORS setup

FastAPI application for The Aerospace Company Customer Service Agent
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from contextlib import asynccontextmanager

from app.routers import health, collections, upload, sessions, chat
from app.retrieval.chroma_client import initialize_knowledge_bases
from app.utils.config import config
from app.utils.logger import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    app_logger.info("Starting application...")
    
    # Validate configuration
    config_errors = config.validate()
    if config_errors:
        app_logger.error(f"Configuration errors: {config_errors}")
        raise ValueError(f"Configuration errors: {config_errors}")
    
    # Initialize ChromaDB collections
    try:
        app_logger.info("Initializing ChromaDB collections...")
        initialize_knowledge_bases()
        app_logger.info("ChromaDB knowledge bases initialized successfully")
    except Exception as e:
        app_logger.error(f"Failed to initialize ChromaDB collections: {e}")
        raise
    
    app_logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    app_logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title="The Aerospace Company Customer Service Agent API",
    description="Multi-agent AI system API for customer service representatives",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add process time middleware
@app.middleware("http")
async def add_process_time_middleware(request, call_next):
    """Add process time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(health.router)
app.include_router(collections.router)
app.include_router(upload.router)
app.include_router(sessions.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "The Aerospace Company Customer Service Agent API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
    )

