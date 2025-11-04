# The Aerospace Company Customer Service Agent

A sophisticated, proof-of-concept multi-agent AI system built with LangChain v1.0 that assists internal customer service representatives by intelligently routing customer inquiries to specialized AI agents.

## 📚 Single Source of Information

This README.md file serves as the **single source of information** for:

- **Setting up the application** - Complete environment setup, installation, and configuration instructions
- **Running the application** - Both manual and automated restart scripts for starting backend and frontend servers
- **Uploading and testing documents** - Comprehensive guide for document upload, Auto-Map feature, and test document creation
- **Verification and troubleshooting** - Health checks, verification steps, and detailed troubleshooting for common issues
- **Quick reference for all URLs and endpoints** - Complete table of all service URLs, API endpoints, and status checks

All instruction files have been consolidated into this comprehensive README for easy navigation and reference.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Knowledge Base Setup](#knowledge-base-setup)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Recent Updates](#recent-updates)

## 🎯 Overview

This system uses a **supervisor pattern** where an orchestrator agent coordinates specialized worker agents:
- **Billing Tool Agent:** Hybrid RAG/CAG for dynamic pricing queries and cached policy information
- **Technical Tool Agent:** Pure RAG for dynamic technical documentation and bug reports
- **Policy Tool Agent:** Pure CAG for consistent, fast responses from static regulatory documents

The system provides real-time streaming responses, maintains conversation history, and includes emergency escalation for safety-critical queries.

## ✨ Features

- **Multi-Agent AI System:** Intelligent routing to specialized agents based on query intent
- **Real-Time Streaming:** Server-Sent Events (SSE) for real-time response streaming
- **Knowledge Base Management:** Document upload with Auto-Map categorization or manual selection
- **Conversation History:** FIFO retention of last 3 conversations per representative
- **Emergency Escalation:** Automatic detection and escalation for safety-critical queries
- **Satisfaction Feedback:** Thumbs up/down voting with optional feedback comments
- **Source Citations:** All responses include source citations for verification
- **Token Usage Tracking:** Real-time tracking of input and output tokens with cost calculation
- **Interactive Tooltips:** Detailed breakdowns for token counts and cost calculations with tooltip information

## 🛠 Technology Stack

### Backend
- **Python:** 3.11+
- **FastAPI:** Modern, fast web framework for building APIs
- **LangChain:** v1.0+ (AI framework)
- **LangGraph:** Agent orchestration
- **ChromaDB:** 0.4+ (Vector database for knowledge bases)
- **OpenAI API:** GPT-4o-mini (for worker agents) and text-embedding-3-small (embeddings)
- **AWS Bedrock:** Claude 3 Haiku or Nova Lite (for supervisor routing)

### Frontend
- **Next.js:** 16.0.1
- **React:** 19.2.0
- **TailwindCSS:** 4.x (Styling)
- **lucide-react:** Icon library for UI components
- **TypeScript:** Type-safe JavaScript

### Development Tools
- **Uvicorn:** ASGI server for FastAPI
- **Pydantic:** Data validation
- **LangSmith:** Optional tracing and debugging

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Node.js 18.x+ and npm**
   ```bash
   node --version  # Should be 18.x or higher
   npm --version
   ```

3. **OpenAI API Key**
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Generate an API key from your dashboard

4. **AWS Account with Bedrock Access**
   - AWS account with Bedrock enabled
   - AWS Access Key ID and Secret Access Key
   - Appropriate IAM permissions for Bedrock

5. **Git** (for cloning the repository)

## 📁 Project Structure

```
agentic-customer-project/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── dependencies.py  # Shared dependencies
│   │   ├── agents/          # Agent implementations
│   │   │   ├── orchestrator.py      # Supervisor agent
│   │   │   ├── billing_agent.py     # Billing Tool Agent
│   │   │   ├── technical_agent.py   # Technical Tool Agent
│   │   │   └── policy_agent.py      # Policy Tool Agent
│   │   ├── retrieval/       # RAG/CAG retrieval implementations
│   │   │   ├── chroma_client.py
│   │   │   ├── rag_retriever.py
│   │   │   ├── cag_retriever.py
│   │   │   └── hybrid_retriever.py
│   │   ├── ingestion/       # Document ingestion pipeline
│   │   │   ├── ingest_data.py
│   │   │   ├── parsers/
│   │   │   ├── chunkers/
│   │   │   └── embeddings/
│   │   ├── api/             # API routes
│   │   │   ├── chat.py      # POST /chat endpoint
│   │   │   ├── upload.py    # POST /upload endpoint
│   │   │   ├── sessions.py   # Session management endpoints
│   │   │   ├── feedback.py  # POST /feedback endpoint
│   │   │   ├── collections.py # GET /collections endpoint
│   │   │   └── health.py    # GET /health endpoint
│   │   ├── schema/          # Pydantic schemas
│   │   │   ├── chat.py
│   │   │   ├── upload.py
│   │   │   └── session.py
│   │   ├── state/           # Conversation state management
│   │   │   └── conversation_state.py
│   │   └── utils/           # Utility functions
│   │       ├── logger.py
│   │       └── config.py
│   ├── tests/               # Backend tests (199 tests total)
│   │   ├── README_TESTING.md # Testing documentation
│   │   └── TEST_RESULTS.md   # Test results summary
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Example environment variables
│
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   │   ├── page.tsx     # Main chat interface
│   │   │   ├── upload.tsx   # Document upload page
│   │   │   └── dashboard.tsx # Session management
│   │   ├── components/      # React components
│   │   │   ├── ChatInterface/
│   │   │   ├── DocumentUpload/
│   │   │   ├── SessionManager/
│   │   │   └── common/
│   │   ├── hooks/           # Custom React hooks
│   │   │   ├── useChat.ts
│   │   │   ├── useUpload.ts
│   │   │   └── useSession.ts
│   │   ├── utils/           # Utility functions
│   │   │   ├── api-client.ts
│   │   │   ├── file-handlers.ts
│   │   │   └── stream-parser.ts
│   │   └── styles/          # Global styles
│   │       └── globals.css
│   ├── public/              # Static assets
│   ├── tests/               # Frontend tests (81 tests total)
│   │   ├── README_TESTING.md # Testing documentation
│   │   └── TEST_RESULTS.md   # Test results summary
│   ├── package.json         # Node.js dependencies
│   ├── tsconfig.json        # TypeScript configuration
│   ├── next.config.js        # Next.js configuration
│   └── .env.example         # Example environment variables
│
├── tasks/                   # Project documentation
│   └── 0001-prd-aerospace-customer-service.md
│
├── supplemental-docs/       # Additional documentation
│
├── chroma_db/               # ChromaDB vector database (created on first run)
│
├── .gitignore
└── README.md                # This file
```

## 🔧 Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agentic-customer-project
```

### 2. Backend Environment Setup

1. **Create Python Virtual Environment**

   ```bash
   # Navigate to backend directory
   cd backend

   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

2. **Create `.env` File**

   Create a `.env` file in the `backend/` directory:

   ```bash
   cd backend
   cp .env.example .env  # If .env.example exists
   # Or create .env manually
   ```

   Add the following environment variables:

   ```env
   # Required Environment Variables
   OPENAI_API_KEY=your_openai_api_key_here
   AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
   AWS_REGION=us-east-1
   ESCALATION_EMAIL=john.doe@aerospace-co.com

   # Optional Environment Variables (for LangSmith tracing)
   LANGSMITH_TRACING=false
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_PROJECT=aerospace-customer-service
   ```

### 3. Frontend Environment Setup

1. **Create `.env.local` File**

   Create a `.env.local` file in the `frontend/` directory:

   ```bash
   cd frontend
   cp .env.example .env.local  # If .env.example exists
   # Or create .env.local manually
   ```

   Add the following environment variables:

   ```env
   # Backend API URL
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## 📥 Installation

### Backend Installation

1. **Navigate to backend directory and activate virtual environment**

   ```bash
   cd backend
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate    # On Windows
   ```

2. **Install Python dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   **Note:** If `requirements.txt` doesn't exist yet, install core dependencies:

   ```bash
   pip install fastapi uvicorn langchain langgraph langchain-openai langchain-aws chromadb pydantic python-dotenv
   ```

3. **Verify Installation**

   ```bash
   python -c "import fastapi; import langchain; print('Installation successful!')"
   ```

### Frontend Installation

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**

   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Verify Installation**

   ```bash
   npm run build  # This will check if everything is set up correctly
   ```

## 🚀 Running the Application

### Quick Start (Using Restart Scripts)

The easiest way to start both applications is using the restart scripts:

**Option 1: Start Both Applications at Once**
```bash
# From project root
./restart_all.sh
```

**Option 2: Start Applications Separately**

**Backend:**
```bash
cd backend
./restart_backend.sh
```

**Frontend:**
```bash
cd frontend
./restart_frontend.sh
```

### Manual Start Instructions

#### 1. Start the Backend Server

**Terminal 1:**

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate    # On Windows

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

✅ **Backend is running at:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Health Check:** http://localhost:8000/health
- **Alternative Docs:** http://localhost:8000/redoc (ReDoc)

#### 2. Start the Frontend Development Server

**Terminal 2 (New Terminal):**

```bash
# Navigate to frontend directory
cd frontend

# Start Next.js development server
npm run dev
# or
yarn dev
# or
pnpm dev
```

**Expected Output:**
```
▲ Next.js 16.0.1
- Local:        http://localhost:3000
```

✅ **Frontend is running at:** http://localhost:3000

#### 3. Access the Application

Open your browser and navigate to:
- **Main Chat Interface:** http://localhost:3000
- **Document Upload Page:** http://localhost:3000/upload
- **Backend API Docs:** http://localhost:8000/docs

## 📡 API Endpoints

### Chat Endpoints

- **POST /chat** - Submit a chat message and receive streaming response
  - Request: `{ "session_id": str, "message": str, "stream": bool }`
  - Response: Server-Sent Events (SSE) stream

- **GET /sessions** - Get list of last 3 conversations
  - Response: `{ "sessions": [Session], "total": int }`

- **GET /sessions/{session_id}** - Get conversation history for a session
  - Response: `{ "session_id": str, "history": [Message], "metadata": {} }`

- **DELETE /sessions/{session_id}** - Delete a conversation session

### Document Management Endpoints

- **POST /upload** - Upload documents to knowledge base
  - Request: multipart/form-data with files and optional `target_collection`
  - Response: `{ "upload_id": str, "status": "queued", "files": [...] }`

- **GET /collections** - Get list of available knowledge base collections
  - Response: `{ "collections": ["billing_knowledge_base", "technical_knowledge_base", "policy_knowledge_base"] }`

- **GET /upload/status/{upload_id}** - Get upload progress status

### Feedback Endpoint

- **POST /feedback** - Submit satisfaction feedback
  - Request: `{ "session_id": str, "rating": "thumbs_up" | "thumbs_down", "comment": str | null }`
  - Response: `{ "success": bool, "message": str }`

### Health Endpoint

- **GET /health** - Check system health
  - Response: `{ "status": "healthy", "timestamp": timestamp }`

For detailed API documentation, visit http://localhost:8000/docs after starting the backend server.

## 🗄️ Knowledge Base Setup

### Initial Knowledge Base Population

Before using the system, you'll need to populate the knowledge bases with documents. This section provides comprehensive instructions for document upload and testing.

### Knowledge Base Collections

The system uses three separate knowledge base collections:

- **billing_knowledge_base:** Parts catalogs, contracts, invoices, pricing policies
- **technical_knowledge_base:** Bug reports, technical manuals, specifications, technical publications
- **policy_knowledge_base:** FAA/EASA regulations, government policies, DFARs, data governance, customer support policies

### Uploading Documents

#### Method 1: Web Interface (Recommended)

1. **Navigate to Upload Page**
   - Go to: **http://localhost:3000/upload**
   - Or click the upload link in the main interface

2. **Select Knowledge Base**
   - Choose from dropdown:
     - **Auto-Map** (default) - Automatically categorizes documents based on content
     - **Billing Knowledge Base** - For invoices, contracts, pricing documents
     - **Technical Knowledge Base** - For manuals, bug reports, specifications
     - **Policy Knowledge Base** - For regulations, policies, compliance docs

3. **Upload Documents**
   - **Method 1:** Click the upload area and select files
   - **Method 2:** Drag and drop files onto the upload area
   - **Supported Formats:** PDF (.pdf), Text (.txt), Markdown (.md), JSON (.json)
   - **File Size Limit:** ~100 KB per file (target)

4. **Monitor Upload Progress**
   - View real-time progress for each file
   - See chunk count after successful upload
   - Check for any errors

5. **Verify Upload Success**
   - Files should show "success" status
   - Chunks count should be displayed (e.g., "5 chunks")
   - Target collection shown correctly
   - No error messages

#### Method 2: API Direct (curl)

**Upload a single file:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@/path/to/your/document.pdf" \
  -F "target_collection=auto-map"
```

**Upload multiple files:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@/path/to/document1.pdf" \
  -F "files=@/path/to/document2.txt" \
  -F "target_collection=billing_knowledge_base"
```

**Check upload status:**
```bash
# Replace {upload_id} with the ID from the upload response
curl http://localhost:8000/upload/status/{upload_id}
```

### Testing Auto-Map Feature

The **Auto-Map** feature analyzes document content and automatically categorizes documents:

| Document Type | Keywords | Maps To |
|--------------|----------|---------|
| **Billing** | invoice, payment, contract, pricing, billing | `billing_knowledge_base` |
| **Technical** | installation, troubleshooting, manual, specification, bug | `technical_knowledge_base` |
| **Policy** | policy, compliance, regulation, governance, requirement | `policy_knowledge_base` |

**To test Auto-Map:**
1. Select **"Auto-Map"** in dropdown
2. Upload test documents (invoice, manual, policy)
3. Watch them get categorized automatically
4. Verify `target_collection` in upload status

### Creating Test Documents

You can create sample test documents for testing:

**Billing Document (test_invoice.txt):**
```bash
cat > test_invoice.txt << 'EOF'
Invoice #12345
Customer: Test Aerospace Corp
Date: 2025-01-15
Amount: $10,000.00

Items:
- Part A123: $5,000.00
- Part B456: $5,000.00

Payment Terms: Net 30
Contract: C-2024-001
EOF
```

**Technical Document (test_manual.txt):**
```bash
cat > test_manual.txt << 'EOF'
Technical Manual: System XYZ
Version: 2.0

Installation:
1. Unpack files
2. Run setup.sh
3. Configure database

Troubleshooting:
- Error 404: Check database connection
- Error 500: Verify file permissions

Specifications:
- CPU: 4 cores minimum
- RAM: 8GB minimum
EOF
```

**Policy Document (test_policy.txt):**
```bash
cat > test_policy.txt << 'EOF'
Policy Document: Data Governance
Effective Date: 2025-01-01

Compliance Requirements:
- GDPR compliance for EU customers
- CCPA compliance for California customers
- DFARs compliance for government contracts

Data Retention: 7 years
Security: Encryption at rest and in transit
EOF
```

### Verification Steps

After uploading documents, verify they were ingested correctly:

**1. Check Health Endpoint**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "chromadb": {
    "connected": true,
    "collections_count": 3,
    "collections": [
      "billing_knowledge_base",
      "technical_knowledge_base",
      "policy_knowledge_base"
    ]
  },
  "timestamp": "2025-01-15T10:00:00"
}
```

**2. Check Collections Endpoint**
```bash
curl http://localhost:8000/collections
```

**Expected Response:**
```json
{
  "collections": [
    "billing_knowledge_base",
    "technical_knowledge_base",
    "policy_knowledge_base"
  ],
  "configured": [...],
  "count": 3
}
```

**3. Verify in Web UI**
- Files show "success" status
- Chunks count displayed (e.g., "5 chunks")
- Target collection shown correctly
- No error messages

### Expected Upload Flow

1. **File Selection**
   - Files appear in preview list
   - Status shows "pending"

2. **Upload Process**
   - Status changes to "uploading"
   - Progress percentage increases
   - Real-time updates via polling

3. **Ingestion Process**
   - Status: "processing"
   - File parsed (PDF, TXT, MD, JSON)
   - Content chunked
   - Embeddings generated
   - Documents stored in ChromaDB

4. **Completion**
   - Status changes to "success"
   - Chunks count displayed
   - Target collection shown
   - Documents ready for retrieval

### Upload Test Checklist

Use this checklist to verify upload functionality:

- [ ] Backend server is running (Terminal 1)
- [ ] Frontend server is running (Terminal 2)
- [ ] Can access http://localhost:3000/upload
- [ ] Can select knowledge base from dropdown
- [ ] Can select files (PDF, TXT, MD, JSON)
- [ ] Upload progress shows correctly
- [ ] Files show "success" status after upload
- [ ] Chunks count is displayed
- [ ] Collections endpoint shows 3 collections
- [ ] Health endpoint shows ChromaDB connected
- [ ] Auto-Map categorizes documents correctly

### Next Steps After Upload

Once documents are successfully uploaded:

1. **Test Chat Interface**
   - Go to http://localhost:3000
   - Ask questions related to uploaded documents
   - Verify agents can retrieve information from the knowledge bases

2. **Test Knowledge Base Queries**
   - Ask billing-related questions → Should route to Billing Agent
   - Ask technical questions → Should route to Technical Agent
   - Ask policy questions → Should route to Policy Agent

3. **Verify Agent Routing**
   - Test multi-part queries that require multiple agents
   - Verify contributing agents and models are displayed correctly
   - Check that token usage and cost are tracked properly

## 💻 Development Guidelines

### Development Methodology

This project follows the **Vibe Coding Strategy**:
- Natural language-driven, iterative approach
- Developer acts as "conductor," guiding and validating AI-generated output
- Conversational loop with AI tools generating code
- NO MAX MODE - use standard AI assistance patterns

### Code Style

- **Backend:** Follow PEP 8 Python style guide
- **Frontend:** Follow Next.js and React best practices
- **TypeScript:** Use strict type checking
- **Commits:** Use conventional commit messages

### LangChain v1.0 Best Practices

- Use `create_agent()` from `langchain.agents` for all agents
- Implement supervisor pattern with tool calling
- Use `@tool` decorator for worker agents and RAG tools
- Use `InMemorySaver()` for conversation persistence
- Pass `thread_id` in config for session management

### Testing

Both backend and frontend have comprehensive test suites with 100% pass rates.

#### Backend Tests (199 tests - 100% pass rate)

```bash
cd backend
pytest tests/ -v
```

Test files are located in `backend/tests/`:
- Unit tests for all modules
- Integration tests for API endpoints
- Agent tests (Supervisor, Policy, Technical, Billing)
- Connection tests (OpenAI, AWS Bedrock)
- Multi-agent routing tests

For detailed test documentation, see `backend/tests/README_TESTING.md` and `backend/tests/TEST_RESULTS.md`.

#### Frontend Tests (81 tests - 100% pass rate)

```bash
cd frontend
npm test
```

Test files are located in `frontend/tests/`:
- Component tests with React Testing Library
- Hook tests (useChat, useUpload, useSession)
- Context provider tests
- Service tests (API client)

For detailed test documentation, see `frontend/tests/README_TESTING.md` and `frontend/tests/TEST_RESULTS.md`.

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**
   - Verify Python version is 3.11+
   - Ensure virtual environment is activated
   - Check that all environment variables are set in `.env`
   - Verify OpenAI and AWS credentials are correct

2. **Frontend won't connect to backend**
   - Verify backend is running on http://localhost:8000
   - Check `NEXT_PUBLIC_API_URL` in `.env.local`
   - Check CORS settings in FastAPI backend

3. **ChromaDB errors**
   - Ensure ChromaDB directory exists (created automatically on first run)
   - Check write permissions in project directory
   - Verify embeddings model is accessible

4. **LLM API errors**
   - Verify API keys are set correctly
   - Check API quotas and rate limits
   - Ensure AWS Bedrock is enabled in your region
   - Verify IAM permissions for Bedrock access

5. **Document upload fails**
   - Check file size limits (target: ~100 KB per file, 100 files per collection)
   - Verify file formats are supported (PDF, TXT, Markdown, JSON)
   - Check ChromaDB connection
   - Verify backend is running on http://localhost:8000
   - Check backend logs for parsing or embedding errors
   - Verify OpenAI API key is valid and has quota

6. **Documents not appearing after upload**
   - Verify ChromaDB connection (check `/health` endpoint)
   - Check collections exist (check `/collections` endpoint)
   - Verify upload completed successfully (check upload status)
   - Check backend logs for ingestion errors
   - Verify OpenAI API quota/rate limits

### Quick Reference Table

| Service | URL | Purpose | Status Check |
|---------|-----|---------|--------------|
| **Main Chat Interface** | http://localhost:3000 | Chat with AI agents | Visual UI |
| **Upload Page** | http://localhost:3000/upload | Upload documents | Visual UI |
| **Backend API** | http://localhost:8000 | REST API | http://localhost:8000/health |
| **API Docs** | http://localhost:8000/docs | Swagger UI | Browser |
| **Health Check** | http://localhost:8000/health | System status | GET |
| **Collections** | http://localhost:8000/collections | List knowledge bases | GET |
| **Upload API** | http://localhost:8000/upload | Upload documents | POST |
| **Upload Status** | http://localhost:8000/upload/status/{id} | Check upload progress | GET |

### Getting Help

- Check the API documentation at http://localhost:8000/docs
- Review the PRD: `tasks/0001-prd-aerospace-customer-service.md`
- Check backend logs in Terminal 1 (backend)
- Check frontend console in browser DevTools
- Review troubleshooting sections in `backend/README.md` and `frontend/README.md`

## 🤝 Contributing

This is a proof-of-concept project. For development guidelines:

1. Follow the Vibe Coding Strategy methodology
2. Maintain code quality and documentation
3. Write tests for new features
4. Update this README when adding new setup steps

## 📄 License

[Add your license information here]

## 📞 Support

For issues or questions:
- Emergency Escalation: **john.doe@aerospace-co.com**
- Review project documentation in `tasks/` and `supplemental-docs/`

---

**Last Updated:** November 3, 2025  
**Version:** 1.0

---

## 📝 Recent Updates (November 3, 2025)

### Critical Bug Fixes ✅
- **Contributing Agents Reinitialization:** Fixed accumulation bug across requests using tool_call ID tracking
- **Billing KB Retrieval:** Increased k from 3 to 5 for comprehensive invoice retrieval  
- **Order Preservation:** Agents/models now display in exact invocation sequence

### UI/UX Enhancements ✅
- **Contributing Display:** Same-line format with `||` separator, bold titles, normal values
- **Centered Layouts:** Satisfaction feedback and upload dialog properly centered
- **Wider Message Boxes:** Increased width by 33% (max-w-4xl → max-w-6xl)
- **Token Usage Tracking:** Real-time tracking of input and output tokens with cost calculation
- **Interactive Tooltips:** 
  - Token count tooltip shows breakdown of what's included in input/output tokens
  - Cost tooltip shows pricing model (Claude 3 Haiku) and unit prices
- **Restart Scripts:** Easy application restart with `restart_all.sh`, `restart_backend.sh`, and `restart_frontend.sh`

### Technical Improvements ✅
- Tool call ID tracking (`tool_call.id`) for reliable deduplication
- Lists instead of sets preserve invocation order
- Explicit array initialization prevents localStorage persistence issues
- Comprehensive document retrieval for comparative queries

### Documentation Updates ✅
- **Documentation Consolidation:** Merged all instruction files (START_APPLICATION.md, RUN_INSTRUCTIONS.md, QUICK_START_UPLOAD.md, HOW_TO_TEST_UPLOAD.md, TEST_DOCUMENT_UPLOAD.md) into comprehensive README
- Enhanced Knowledge Base Setup section with detailed upload instructions
- Added comprehensive verification steps and troubleshooting for document uploads
- Added quick reference table for all application URLs

---

