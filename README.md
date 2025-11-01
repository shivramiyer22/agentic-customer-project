# The Aerospace Company Customer Service Agent

A sophisticated, proof-of-concept multi-agent AI system built with LangChain v1.0 that assists internal customer service representatives by intelligently routing customer inquiries to specialized AI agents.

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
- [Development Guidelines](#development-guidelines)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This system uses a **supervisor pattern** where an orchestrator agent coordinates specialized worker agents:
- **Billing Support Agent:** Hybrid RAG/CAG for dynamic pricing queries and cached policy information
- **Technical Support Agent:** Pure RAG for dynamic technical documentation and bug reports
- **Policy & Compliance Agent:** Pure CAG for consistent, fast responses from static regulatory documents

The system provides real-time streaming responses, maintains conversation history, and includes emergency escalation for safety-critical queries.

## ✨ Features

- **Multi-Agent AI System:** Intelligent routing to specialized agents based on query intent
- **Real-Time Streaming:** Server-Sent Events (SSE) for real-time response streaming
- **Knowledge Base Management:** Document upload with Auto-Map categorization or manual selection
- **Conversation History:** FIFO retention of last 3 conversations per representative
- **Emergency Escalation:** Automatic detection and escalation for safety-critical queries
- **Satisfaction Feedback:** Thumbs up/down voting with optional feedback comments
- **Source Citations:** All responses include source citations for verification

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
- **Next.js:** 14.x
- **React:** 18.x
- **shadcn/ui:** Modern UI component library
- **TailwindCSS:** 3.x (Styling)
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
│   │   │   ├── billing_agent.py     # Billing Support Agent
│   │   │   ├── technical_agent.py   # Technical Support Agent
│   │   │   └── policy_agent.py      # Policy & Compliance Agent
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
│   ├── tests/               # Backend tests
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

### 1. Start the Backend Server

1. **Navigate to backend directory and activate virtual environment**

   ```bash
   cd backend
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate    # On Windows
   ```

2. **Start FastAPI server**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend API will be available at:
   - **API:** http://localhost:8000
   - **API Docs:** http://localhost:8000/docs (Swagger UI)
   - **Alternative Docs:** http://localhost:8000/redoc (ReDoc)

### 2. Start the Frontend Development Server

1. **Navigate to frontend directory** (in a new terminal)

   ```bash
   cd frontend
   ```

2. **Start Next.js development server**

   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

   The frontend will be available at:
   - **Frontend:** http://localhost:3000

### 3. Access the Application

Open your browser and navigate to:
- **Application:** http://localhost:3000
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

Before using the system, you'll need to populate the knowledge bases with documents. You can:

1. **Use the Upload Interface**
   - Navigate to the upload page in the frontend
   - Select documents (PDF, TXT, Markdown, JSON)
   - Choose "Auto-Map" for automatic categorization or manually select a knowledge base
   - Upload documents

2. **Use the Ingestion Script** (if available)
   ```bash
   cd backend
   python scripts/ingest_data.py --directory ./documents --collection billing_knowledge_base
   ```

### Knowledge Base Collections

- **billing_knowledge_base:** Parts catalogs, contracts, invoices, pricing policies
- **technical_knowledge_base:** Bug reports, technical manuals, specifications, technical publications
- **policy_knowledge_base:** FAA/EASA regulations, government policies, DFARs, data governance, customer support policies

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

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

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

### Getting Help

- Check the API documentation at http://localhost:8000/docs
- Review the PRD: `tasks/0001-prd-aerospace-customer-service.md`
- Check architecture documentation: `ARCHITECTURE.md`

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

**Last Updated:** November 2025  
**Version:** 1.0

