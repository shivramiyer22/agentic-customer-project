# Backend API - The Aerospace Company Customer Service Agent

FastAPI backend application for the multi-agent AI customer service system.

**Version:** 1.0.0  
**Framework:** FastAPI  
**Python Version:** 3.11+

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## Overview

This backend application provides REST API endpoints for:

- **Document Ingestion:** Upload and process documents (PDF, TXT, Markdown, JSON) into ChromaDB vector stores
- **Knowledge Base Management:** Three separate collections for billing, technical support, and policy compliance
- **Chat Interface:** API endpoints for chat interactions with streaming support (Server-Sent Events)
- **Session Management:** In-memory session tracking for conversations
- **Health Monitoring:** System health and ChromaDB connectivity checks

The application uses:
- **FastAPI** for REST API framework
- **ChromaDB** for vector database storage
- **LangChain v1.0+** for agent orchestration (to be implemented)
- **OpenAI** for embeddings (text-embedding-3-small)
- **AWS Bedrock** for LLM routing (optional, to be implemented)

---

## Features

### ✅ Implemented

- ✅ Document upload and ingestion pipeline
- ✅ ChromaDB integration with three knowledge base collections
- ✅ File parsing (PDF, TXT, Markdown, JSON)
- ✅ Text chunking with RecursiveCharacterTextSplitter
- ✅ OpenAI embeddings generation
- ✅ Upload progress tracking
- ✅ Collection auto-mapping based on content
- ✅ Session management (CRUD operations)
- ✅ **Supervisor Agent (Orchestrator) - Task 5.0** ✅
  - ✅ Supervisor agent using `create_agent()` from LangChain v1.0
  - ✅ AWS Bedrock integration (with OpenAI fallback)
  - ✅ Emergency detection tool
  - ✅ Worker agent tools (policy implemented, billing/technical placeholders)
  - ✅ Conversation state management with InMemorySaver
  - ✅ SSE streaming support from supervisor agent
  - ✅ Session ID generation and thread_id management
- ✅ **Policy Tool Agent (Pure CAG) - Task 6.0** ✅
  - ✅ Policy agent using `create_agent()` from LangChain v1.0
  - ✅ Pure CAG retrieval strategy (search_policy_kb tool)
  - ✅ OpenAI model (gpt-4o-mini) with descriptive name
  - ✅ CAG retrieval tool for policy_knowledge_base collection
  - ✅ Source citation formatting
  - ✅ Policy tool integration with supervisor agent
  - ✅ Conversation state management with InMemorySaver
- ✅ **Technical Tool Agent (Pure RAG) - Task 7.0** ✅
  - ✅ Technical agent using `create_agent()` from LangChain v1.0
  - ✅ Pure RAG retrieval strategy (search_technical_kb tool)
  - ✅ OpenAI model (gpt-4o-mini) with descriptive name
  - ✅ RAG retrieval tool for technical_knowledge_base collection
  - ✅ Source citation formatting
  - ✅ Technical tool integration with supervisor agent
  - ✅ Conversation state management with InMemorySaver
- ✅ **Billing Tool Agent (Hybrid RAG/CAG) - Task 8.0** ✅
  - ✅ Billing agent using `create_agent()` from LangChain v1.0
  - ✅ Hybrid RAG/CAG retrieval strategy (search_billing_kb and get_cached_policy_info tools)
  - ✅ OpenAI model (gpt-4o-mini) with descriptive name
  - ✅ RAG retrieval tool for billing_knowledge_base collection
  - ✅ CAG caching tool for static policy information with session state management
  - ✅ Source citation formatting
  - ✅ Billing tool integration with supervisor agent
  - ✅ Conversation state management with InMemorySaver
- ✅ Chat endpoint with SSE streaming support
- ✅ Contributing agents and models tracking
- ✅ Token usage tracking and cost calculation
- ✅ Health and collection monitoring endpoints
- ✅ Comprehensive test suite (199 tests total: 32 Task 5.0 + 26 Task 6.0 + 26 Task 7.0 + 28 Task 8.0 + 8 Task 8.13 + 3 Contributing Models + 5 Connection Tests)
- ✅ Complete multi-agent system routing verified
- ✅ AWS Bedrock connection (mandatory) with OpenAI fallback

### ✅ Additional Features

- ✅ Restart script (`restart_backend.sh`) for easy application restart
- ✅ AWS Bedrock Claude 3 Haiku integration for supervisor agent
- ✅ Contributing agents and models tracking in chat responses (with order preservation)
- ✅ Multi-agent routing with emergency detection
- ✅ Tool call ID tracking for reliable agent contribution tracking
- ✅ Billing KB comprehensive retrieval (k=5 for comparative queries)

### 🚧 Future Enhancements

- 🚧 LangSmith tracing integration (optional)
- 🚧 Additional agent specializations if needed

---

## Requirements

### System Requirements

- **Python:** 3.11 or higher
- **Operating System:** macOS, Linux, or Windows
- **Memory:** Minimum 4GB RAM (8GB+ recommended for document processing)
- **Disk Space:** ~1GB for dependencies, plus space for ChromaDB storage

### Python Packages

All dependencies are listed in `requirements.txt`. Key packages include:

- `fastapi>=0.115.0` - Web framework
- `uvicorn[standard]>=0.32.0` - ASGI server
- `langchain>=0.2.0` - LangChain v1.0+
- `chromadb>=0.4.0` - Vector database
- `openai>=1.0.0` - OpenAI API client
- `pydantic>=2.0.0` - Data validation
- `python-multipart>=0.0.9` - File upload support
- `pytest>=7.4.0` - Testing framework

---

## Installation

### 1. Clone the Repository

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
# Using venv (recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
# Edit .env with your configuration
```

See [Environment Variables](#environment-variables) section for details.

### 5. Verify Installation

```bash
python -c "import fastapi, chromadb, langchain; print('✓ Dependencies installed')"
```

### 6. (Optional) Install AWS Support for Bedrock

If you want to use AWS Bedrock (recommended for supervisor agent):

```bash
# langchain-aws should already be in requirements.txt
pip install langchain-aws>=0.1.0
```

---

## Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

### Required

```env
# OpenAI API Key (Required)
OPENAI_API_KEY=your-openai-api-key-here
```

### Optional (with defaults)

```env
# OpenAI Embedding Configuration
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_EMBEDDING_DIMENSIONS=1536

# AWS Bedrock Configuration (Recommended - for supervisor agent)
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=bedrock:claude-3-haiku

# ChromaDB Configuration
CHROMA_DB_PATH=./chroma_db

# Application Configuration
ESCALATION_EMAIL=ski@aerospace-co.com
API_HOST=0.0.0.0
API_PORT=8000

# LangSmith Configuration (Optional - for tracing)
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT=aerospace-customer-service
```

**Note:** If AWS Bedrock credentials are not provided, the supervisor agent will fall back to OpenAI `gpt-4o-mini`. However, AWS Bedrock Claude 3 Haiku is **mandatory** for production use as per project requirements.

### Environment Variable Descriptions

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | OpenAI API key for embeddings |
| `OPENAI_EMBEDDING_MODEL` | No | `text-embedding-3-small` | Embedding model name |
| `OPENAI_EMBEDDING_DIMENSIONS` | No | `1536` | Embedding dimensions |
| `AWS_ACCESS_KEY_ID` | No | - | AWS access key for Bedrock |
| `AWS_SECRET_ACCESS_KEY` | No | - | AWS secret key for Bedrock |
| `AWS_REGION` | No | `us-east-1` | AWS region for Bedrock |
| `CHROMA_DB_PATH` | No | `./chroma_db` | ChromaDB storage path |
| `ESCALATION_EMAIL` | No | `ski@aerospace-co.com` | Emergency escalation email |
| `API_HOST` | No | `0.0.0.0` | API server host |
| `API_PORT` | No | `8000` | API server port |
| `LANGSMITH_TRACING` | No | `false` | Enable LangSmith tracing |
| `LANGSMITH_API_KEY` | No | - | LangSmith API key (if tracing enabled) |
| `LANGSMITH_PROJECT` | No | `aerospace-customer-service` | LangSmith project name |

---

## Running the Application

### Development Mode (with auto-reload)

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Run with production settings
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Python Module

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Using Restart Script

A convenient restart script is available:

```bash
# Make script executable (first time only)
chmod +x restart_backend.sh

# Restart the backend application
./restart_backend.sh
```

This script will:
- Kill any existing processes on port 8000
- Activate the virtual environment
- Start the FastAPI server with auto-reload

**Note:** The script runs the server in the background. Check the output for the process ID if you need to stop it manually.

### Access the API

Once running, the API will be available at:

- **API Base URL:** `http://localhost:8000`
- **Interactive API Docs:** `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)
- **Root Endpoint:** `http://localhost:8000/`

### Startup Sequence

On startup, the application will:

1. ✅ Load and validate environment variables
2. ✅ Initialize ChromaDB client
3. ✅ Create three knowledge base collections:
   - `billing_knowledge_base`
   - `technical_knowledge_base`
   - `policy_knowledge_base`
4. ✅ Start FastAPI server with CORS middleware
5. ✅ Register all API routers

---

## API Endpoints

### Root

- **`GET /`** - Root endpoint with API information
  - Returns: API name, version, docs URL

### Health & Monitoring

- **`GET /health`** - Health check endpoint
  - Returns: System status, ChromaDB connectivity, collection count
  - Example Response:
    ```json
    {
      "status": "healthy",
      "chromadb": {
        "connected": true,
        "collections_count": 3,
        "collections": ["billing_knowledge_base", "technical_knowledge_base", "policy_knowledge_base"]
      },
      "timestamp": "2025-11-01T12:00:00.000000"
    }
    ```

### Collections

- **`GET /collections`** - List all knowledge base collections
  - Returns: Available collections, configured collections, count
  - Example Response:
    ```json
    {
      "collections": ["billing_knowledge_base", "technical_knowledge_base", "policy_knowledge_base"],
      "configured": ["billing_knowledge_base", "technical_knowledge_base", "policy_knowledge_base"],
      "count": 3
    }
    ```

### Document Upload

- **`POST /upload`** - Upload documents for ingestion
  - **Content-Type:** `multipart/form-data`
  - **Parameters:**
    - `files`: List of files (required)
    - `target_collection`: Collection name or "auto-map" (optional, default: "auto-map")
  - **Max File Size:** 20 MB per file
  - **Supported Formats:** PDF, TXT, Markdown (.md), JSON
  - **Returns:** Upload ID, initial status, file details
  - Example Request:
    ```bash
    curl -X POST "http://localhost:8000/upload" \
      -F "files=@document.pdf" \
      -F "files=@manual.txt" \
      -F "target_collection=auto-map"
    ```
  - Example Response:
    ```json
    {
      "upload_id": "upload-abc123",
      "status": "queued",
      "files": [
        {
          "file_name": "document.pdf",
          "file_size": 1024000,
          "status": "queued",
          "progress": 0
        }
      ],
      "overall_progress": 0,
      "created_at": "2025-11-01T12:00:00.000000"
    }
    ```

- **`GET /upload/status/{upload_id}`** - Get upload status
  - **Parameters:** `upload_id` (path parameter)
  - **Returns:** Current upload status, per-file progress, collection mapping
  - Example Response:
    ```json
    {
      "upload_id": "upload-abc123",
      "status": "processing",
      "files": [
        {
          "file_name": "document.pdf",
          "file_size": 1024000,
          "status": "processing",
          "progress": 45,
          "target_collection": "billing_knowledge_base",
          "chunks_count": 12
        }
      ],
      "overall_progress": 45,
      "created_at": "2025-11-01T12:00:00.000000",
      "updated_at": "2025-11-01T12:00:05.000000"
    }
    ```

### Session Management

- **`GET /sessions`** - List all chat sessions
  - Returns: List of sessions with metadata
  - Example Response:
    ```json
    {
      "sessions": [
        {
          "session_id": "session-abc123",
          "created_at": "2025-11-01T12:00:00.000000",
          "updated_at": "2025-11-01T12:30:00.000000",
          "message_count": 5,
          "agent": null
        }
      ],
      "count": 1
    }
    ```

- **`GET /sessions/{session_id}`** - Get specific session
  - **Parameters:** `session_id` (path parameter)
  - Returns: Session details

- **`POST /sessions`** - Create new session
  - **Body (optional):** `{ "session_id": "custom-id" }`
  - Returns: Created session details

- **`DELETE /sessions/{session_id}`** - Delete session
  - **Parameters:** `session_id` (path parameter)
  - Returns: Success message

### Chat

- **`POST /chat`** - Send chat message (with streaming support)
  - **Content-Type:** `application/json`
  - **Body:**
    ```json
    {
      "session_id": "session-abc123",
      "message": "What is the return policy?",
      "stream": true
    }
    ```
  - **Returns:**
    - **Streaming (`stream: true`):** Server-Sent Events (SSE) stream with chunks
    - **Non-streaming (`stream: false`):** JSON response with complete message
  - **Note:** Currently returns placeholder responses. Will be replaced with agent system (Tasks 5-8).

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── health.py           # Health check endpoint
│   │   ├── collections.py      # Collections listing endpoint
│   │   ├── upload.py           # Document upload endpoints
│   │   ├── sessions.py         # Session management endpoints
│   │   └── chat.py             # Chat endpoint (placeholder)
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   └── upload.py           # Upload request/response schemas
│   │
│   ├── ingestion/              # Document ingestion pipeline
│   │   ├── __init__.py
│   │   ├── ingest_data.py      # Main ingestion function
│   │   │
│   │   ├── parsers/            # Document parsers
│   │   │   ├── __init__.py
│   │   │   ├── parser_factory.py  # Parser factory
│   │   │   ├── pdf_parser.py      # PDF parser
│   │   │   ├── txt_parser.py      # Text parser
│   │   │   ├── markdown_parser.py # Markdown parser
│   │   │   └── json_parser.py     # JSON parser
│   │   │
│   │   ├── chunkers/           # Text chunking
│   │   │   ├── __init__.py
│   │   │   └── recursive_chunker.py  # RecursiveCharacterTextSplitter
│   │   │
│   │   └── embeddings/         # Embedding generation
│   │       ├── __init__.py
│   │       └── openai_embedder.py   # OpenAI embeddings
│   │
│   ├── retrieval/              # Vector database and retrieval
│   │   ├── __init__.py
│   │   └── chroma_client.py   # ChromaDB client and collections
│   │
│   ├── agents/                 # Agent implementations (Tasks 5-8)
│   │   ├── __init__.py
│   │   ├── orchestrator.py     # Supervisor agent (planned)
│   │   ├── billing_agent.py    # Billing Tool Agent (planned)
│   │   ├── technical_agent.py  # Technical Tool Agent (planned)
│   │   └── policy_agent.py     # Policy Tool Agent (planned)
│   │
│   └── utils/                   # Utilities
│       ├── __init__.py
│       ├── config.py            # Configuration and environment variables
│       └── logger.py            # Logging configuration
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration
│   ├── test_main.py             # Main application tests
│   ├── test_config.py           # Configuration tests
│   ├── test_chroma_client.py    # ChromaDB client tests
│   ├── test_parsers.py           # Parser tests
│   ├── test_chunkers.py         # Chunker tests
│   ├── test_ingestion.py         # Ingestion pipeline tests
│   ├── test_ingestion_comprehensive.py  # Comprehensive ingestion tests
│   ├── test_routers_health.py    # Health endpoint tests
│   ├── test_routers_collections.py  # Collections endpoint tests
│   ├── test_routers_upload.py   # Upload endpoint tests
│   ├── test_routers.py          # Router tests
│   └── test_integration.py     # Integration tests
│
├── chroma_db/                   # ChromaDB persistent storage
│   └── [collection data files]
│
├── uploads/                     # Temporary upload storage
│   └── [temporary files]
│
├── venv/                        # Virtual environment (git-ignored)
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .env                         # Environment variables (git-ignored)
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

---

## Testing

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run specific test
pytest tests/test_main.py::test_root_endpoint

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Coverage

The test suite includes **194 tests** with **100% pass rate**:

- ✅ Configuration tests (6 tests) - `test_config.py`
- ✅ ChromaDB client tests (4 tests) - `test_chroma_client.py`
- ✅ Document parser tests (10 tests) - `test_parsers.py`
- ✅ Chunker tests (6 tests) - `test_chunkers.py`
- ✅ Ingestion pipeline tests (21 tests) - `test_ingestion.py`, `test_ingestion_comprehensive.py`
- ✅ Router endpoint tests (31 tests) - `test_routers_*.py`
  - Health Router: 3 tests
  - Collections Router: 4 tests
  - Upload Router: 10 tests
  - Chat Router: 11 tests (includes 3 Contributing Models tests)
  - General Router: 2 tests
- ✅ Agent tests (78 tests):
  - Supervisor Agent: 18 tests (includes 2 AWS Bedrock connection tests)
  - Policy Agent: 16 tests
  - Technical Agent: 16 tests
  - Billing Agent: 16 tests
  - Multi-Agent Routing: 8 tests
- ✅ Retrieval tests (31 tests):
  - CAG Retriever: 10 tests
  - RAG Retriever: 10 tests
  - Hybrid Retriever: 11 tests
- ✅ State management tests (3 tests) - `test_state.py`
- ✅ Schema tests (9 tests) - `test_schemas_chat.py`
- ✅ Integration tests (4 tests) - `test_integration.py`

For detailed test documentation, see `README_TESTING.md` and `TEST_RESULTS.md`.

### Test Requirements

Tests require:
- All dependencies from `requirements.txt`
- Valid `OPENAI_API_KEY` in `.env` file (for embedding tests)
- ChromaDB accessible (uses local storage in `chroma_db/`)

---

## Development

### Code Style

- Follow PEP 8 Python style guide
- Use type hints throughout
- Document functions and classes with docstrings
- Use Pydantic models for data validation

### Adding New Endpoints

1. Create router in `app/routers/`
2. Define Pydantic schemas in `app/schemas/`
3. Register router in `app/main.py`
4. Add tests in `tests/test_routers_*.py`

### Adding New Document Parsers

1. Create parser in `app/ingestion/parsers/`
2. Register in `app/ingestion/parsers/parser_factory.py`
3. Add tests in `tests/test_parsers.py`

### ChromaDB Collection Management

Collections are initialized on startup via `initialize_knowledge_bases()` in `app/retrieval/chroma_client.py`.

To add a new collection:
1. Add collection name to `app/utils/config.py`
2. Update `get_all_collections()` method
3. Restart the application

---

## Troubleshooting

### Common Issues

#### 1. ChromaDB Connection Error

**Error:** `Failed to initialize ChromaDB collections`

**Solutions:**
- Check if `CHROMA_DB_PATH` is writable
- Ensure sufficient disk space
- Delete `chroma_db/` directory and restart (will recreate collections)

#### 2. OpenAI API Key Error

**Error:** `OPENAI_API_KEY is required`

**Solutions:**
- Create `.env` file in `backend/` directory
- Add `OPENAI_API_KEY=your-key-here`
- Restart the application

#### 3. Import Errors

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solutions:**
- Ensure virtual environment is activated
- Verify you're in the `backend/` directory
- Reinstall dependencies: `pip install -r requirements.txt`

#### 4. Port Already in Use

**Error:** `Address already in use`

**Solutions:**
- Change `API_PORT` in `.env` file
- Or kill existing process:
  ```bash
  # Find process using port 8000
  lsof -ti:8000 | xargs kill -9
  ```

#### 5. File Upload Size Error

**Error:** `File size exceeds maximum`

**Solutions:**
- Max file size is 20 MB per file
- Split large files or compress them
- Check `MAX_FILE_SIZE` in upload router

#### 6. Upload Status Not Updating

**Solutions:**
- Check server logs for ingestion errors
- Verify ChromaDB is accessible
- Check OpenAI API key is valid
- Review upload status in database (if implemented)

#### 7. AWS Bedrock Connection Failed

**Error:** `Failed to connect to AWS Bedrock` or supervisor agent falls back to OpenAI

**Solutions:**
- Verify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are set in `.env`
- Check `AWS_REGION` is correct (default: `us-east-1`)
- Ensure `langchain-aws` package is installed: `pip install langchain-aws>=0.1.0`
- Verify AWS credentials have Bedrock access permissions
- Check AWS service status and region availability

#### 8. Supervisor Agent Not Routing to Multiple Agents

**Error:** Supervisor only routes to one agent for multi-part queries

**Solutions:**
- Check supervisor agent system prompt in `app/agents/orchestrator.py`
- Verify AWS Bedrock is connected (better routing performance)
- Ensure tool descriptions are clear and specific
- Check server logs for tool call details

#### 9. Contributing Agents/Models Not Displaying or Accumulating

**Error:** Contributing agents/models not shown in chat response metadata or showing accumulated values from previous requests

**Solutions:**
- Verify SSE streaming is working correctly
- Check `ChatStreamChunk` metadata includes `contributing_agents` and `contributing_models`
- Ensure frontend is extracting metadata from SSE messages
- Review `app/routers/chat.py` for tool_call_id tracking logic
- Check that lists (not sets) are used for order preservation
- Verify placeholder messages initialize with empty arrays
- Clear browser localStorage if old values persist: `localStorage.clear()`

#### 10. Billing Agent Returns Wrong Invoice Data

**Error:** Agent returns incorrect invoice for comparative queries ("highest", "largest", etc.)

**Solutions:**
- Verify billing KB has sufficient documents uploaded
- Check k parameter in `search_billing_kb` (default: k=5)
- Ensure all invoice documents are properly ingested
- Review retrieval scores in logs (lower scores = better matches)
- Consider increasing k if you have many invoice documents
- Verify embeddings are generated correctly

### Debug Mode

Enable verbose logging:

```python
# In app/utils/logger.py
logging.basicConfig(level=logging.DEBUG)
```

Or set environment variable:

```bash
export LOG_LEVEL=DEBUG
```

### Logs Location

Logs are printed to stdout/stderr. In production, redirect to log files:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 >> logs/app.log 2>&1
```

### Checking Application Status

#### Verify Backend is Running

```bash
# Health check
curl http://localhost:8000/health

# Check collections
curl http://localhost:8000/collections

# View API docs
open http://localhost:8000/docs
```

#### Check Process Status

```bash
# Find process on port 8000
lsof -ti:8000

# View process details
ps aux | grep uvicorn
```

#### Verify AWS Bedrock Connection

Check the server logs on startup. You should see:
- `Attempting to connect to AWS Bedrock: bedrock:claude-3-haiku` (if credentials are set)
- `Using AWS Bedrock for supervisor agent` (if connection successful)
- `Falling back to OpenAI` (if Bedrock connection fails)

---

## API Documentation

### Interactive Docs

Once the server is running, access interactive API documentation at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These provide:
- Complete API endpoint documentation
- Request/response schemas
- Interactive API testing
- Example requests and responses

### Example API Calls

#### Health Check

```bash
curl http://localhost:8000/health
```

#### List Collections

```bash
curl http://localhost:8000/collections
```

#### Upload Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "files=@document.pdf" \
  -F "target_collection=billing_knowledge_base"
```

#### Create Session

```bash
curl -X POST "http://localhost:8000/sessions" \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Send Chat Message

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-123",
    "message": "What is the return policy?",
    "stream": false
  }'
```

---

## Production Deployment

### Environment Setup

1. Set production environment variables
2. Use production-grade ASGI server (e.g., Gunicorn with Uvicorn workers)
3. Set up reverse proxy (Nginx, Caddy)
4. Enable HTTPS
5. Configure database for session storage (replace in-memory store)
6. Set up monitoring and logging
7. Configure backup for ChromaDB

### Docker (Future)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Application Architecture

### Multi-Agent System

The application uses a **supervisor-worker pattern** for multi-agent orchestration:

1. **Supervisor Agent** (Task 5.0)
   - Uses AWS Bedrock Claude 3 Haiku (mandatory) with OpenAI fallback
   - Routes queries to appropriate worker agents
   - Detects emergencies and escalates
   - Tracks contributing agents and models

2. **Policy Tool Agent** (Task 6.0)
   - Pure CAG (Cached Augmented Generation) retrieval strategy
   - Handles policy and compliance queries
   - Uses OpenAI `gpt-4o-mini`

3. **Technical Tool Agent** (Task 7.0)
   - Pure RAG (Retrieval Augmented Generation) retrieval strategy
   - Handles technical support queries
   - Uses OpenAI `gpt-4o-mini`

4. **Billing Tool Agent** (Task 8.0)
   - Hybrid RAG/CAG retrieval strategy
   - Handles billing and invoice queries
   - Uses OpenAI `gpt-4o-mini`

### Knowledge Base Collections

Three ChromaDB collections store different document types:

- `billing_knowledge_base` - Billing and invoice documents
- `technical_knowledge_base` - Technical support documents
- `policy_knowledge_base` - Policy and compliance documents

### Retrieval Strategies

- **CAG (Cached Augmented Generation):** Static policy documents cached in memory
- **RAG (Retrieval Augmented Generation):** Dynamic vector similarity search
- **Hybrid RAG/CAG:** Combines both strategies for billing queries

## Completion Status

All planned tasks are **✅ COMPLETE**:

- ✅ **Task 5.0:** Supervisor Agent Implementation
- ✅ **Task 6.0:** Policy Tool Agent (Pure CAG)
- ✅ **Task 7.0:** Technical Tool Agent (Pure RAG)
- ✅ **Task 8.0:** Billing Tool Agent (Hybrid RAG/CAG)

The application now provides full multi-agent orchestration with comprehensive testing and documentation.

---

## Support

For issues or questions:

1. Check this README and troubleshooting section
2. Review API documentation at `/docs`
3. Check server logs for error details
4. Review test files for usage examples

---

## License

Proprietary - The Aerospace Company

---

**Last Updated:** November 2, 2025  
**Version:** 1.0.0

---

## Recent Updates (November 2, 2025)

### Bug Fixes
- ✅ Fixed Contributing Agents reinitialization issue (tool_call ID tracking)
- ✅ Fixed Billing KB retrieval for comparative queries (increased k to 5)
- ✅ Order preservation for contributing agents/models (lists instead of sets)

### Enhancements
- ✅ Reliable deduplication using tool_call.id instead of id(msg)
- ✅ Comprehensive billing document retrieval for better accuracy
- ✅ Contributing agents/models display in invocation order

---

