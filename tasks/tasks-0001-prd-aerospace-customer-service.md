# Task List: Aerospace Customer Service AI System

**Based on PRD:** `0001-prd-aerospace-customer-service.md`  
**Date Created:** November 2025  
**Status:** In Progress

---

## Relevant Files

### Frontend Files (Next.js)
- `frontend/src/app/page.tsx` - Main chat interface page using Next.js App Router
- `frontend/src/app/upload/page.tsx` - Document upload page
- `frontend/src/components/ChatInterface/MessageList.tsx` - Component to display conversation messages
- `frontend/src/components/ChatInterface/InputBox.tsx` - Text input component for chat messages
- `frontend/src/components/ChatInterface/StreamingResponse.tsx` - Component to handle SSE streaming responses
- `frontend/src/components/ChatInterface/SatisfactionFeedback.tsx` - Thumbs up/down feedback component
- `frontend/src/components/DocumentUpload/FileUploader.tsx` - File upload component with drag-and-drop
- `frontend/src/components/DocumentUpload/FilePreview.tsx` - Component to preview selected files
- `frontend/src/components/DocumentUpload/UploadProgress.tsx` - Progress indicator for uploads
- `frontend/src/components/DocumentUpload/KnowledgeBaseSelector.tsx` - Dropdown for knowledge base selection
- `frontend/src/layouts/Header.tsx` - Header component with title and airplane logo
- `frontend/src/layouts/Footer.tsx` - Footer component (optional, for consistent layout)
- `frontend/src/layouts/Sidebar.tsx` - Sidebar component for navigation (optional)
- `frontend/src/context/ChatContext.tsx` - Context provider for chat state management
- `frontend/src/context/SessionContext.tsx` - Context provider for session state management
- `frontend/src/hooks/useChat.ts` - Custom hook for chat functionality and SSE streaming
- `frontend/src/hooks/useUpload.ts` - Custom hook for document upload functionality
- `frontend/src/hooks/useSession.ts` - Custom hook for session management
- `frontend/src/services/api-client.ts` - API client utilities for backend communication
- `frontend/src/utils/stream-parser.ts` - Utility to parse SSE stream data
- `frontend/src/utils/file-handlers.ts` - File validation and handling utilities
- `frontend/src/constants/api-endpoints.ts` - API endpoint URLs and constants
- `frontend/src/styles/globals.css` - Global TailwindCSS styles
- `frontend/public/` - Static assets (images, fonts, airplane logo, etc.)
- `frontend/package.json` - Node.js dependencies
- `frontend/tsconfig.json` - TypeScript configuration
- `frontend/next.config.js` - Next.js configuration
- `frontend/.env.local` - Frontend environment variables

### Backend Files (FastAPI)
- `backend/app/__init__.py` - Package initialization file making app a Python package
- `backend/app/main.py` - FastAPI application entry point with CORS setup
- `backend/app/dependencies.py` - Shared dependencies used by routers
- `backend/app/routers/__init__.py` - Package initialization for routers
- `backend/app/routers/chat.py` - POST /chat endpoint with SSE streaming
- `backend/app/routers/upload.py` - POST /upload endpoint for document uploads
- `backend/app/routers/collections.py` - GET /collections endpoint to list knowledge bases
- `backend/app/routers/health.py` - GET /health endpoint for system status
- `backend/app/routers/sessions.py` - Session management endpoints (GET, POST, DELETE)
- `backend/app/routers/feedback.py` - POST /feedback endpoint for satisfaction feedback
- `backend/app/schemas/__init__.py` - Package initialization for schemas
- `backend/app/schemas/chat.py` - Pydantic schemas for chat endpoints
- `backend/app/schemas/upload.py` - Pydantic schemas for upload endpoints
- `backend/app/schemas/session.py` - Pydantic schemas for session management
- `backend/app/agents/__init__.py` - Package initialization for agents
- `backend/app/agents/orchestrator.py` - Supervisor agent implementation using LangChain v1.0
- `backend/app/agents/billing_agent.py` - Billing Support Agent with Hybrid RAG/CAG strategy
- `backend/app/agents/technical_agent.py` - Technical Support Agent with Pure RAG strategy
- `backend/app/agents/policy_agent.py` - Policy & Compliance Agent with Pure CAG strategy
- `backend/app/retrieval/__init__.py` - Package initialization for retrieval
- `backend/app/retrieval/chroma_client.py` - ChromaDB client initialization and collection management
- `backend/app/retrieval/rag_retriever.py` - RAG retrieval tool implementations
- `backend/app/retrieval/cag_retriever.py` - CAG retrieval tool implementations
- `backend/app/retrieval/hybrid_retriever.py` - Hybrid RAG/CAG retrieval implementation
- `backend/app/ingestion/__init__.py` - Package initialization for ingestion
- `backend/app/ingestion/ingest_data.py` - Main document ingestion pipeline
- `backend/app/ingestion/parsers/__init__.py` - Package initialization for parsers
- `backend/app/ingestion/parsers/pdf_parser.py` - PDF document parser
- `backend/app/ingestion/parsers/txt_parser.py` - Plain text document parser
- `backend/app/ingestion/parsers/markdown_parser.py` - Markdown document parser
- `backend/app/ingestion/parsers/json_parser.py` - JSON document parser
- `backend/app/ingestion/chunkers/__init__.py` - Package initialization for chunkers
- `backend/app/ingestion/chunkers/recursive_chunker.py` - Recursive character text chunker
- `backend/app/ingestion/embeddings/__init__.py` - Package initialization for embeddings
- `backend/app/ingestion/embeddings/openai_embedder.py` - OpenAI embedding generator
- `backend/app/state/__init__.py` - Package initialization for state
- `backend/app/state/conversation_state.py` - Conversation state management with InMemorySaver
- `backend/app/utils/__init__.py` - Package initialization for utils
- `backend/app/utils/config.py` - Configuration utilities and environment variable management
- `backend/app/utils/logger.py` - Logging configuration
- `backend/tests/__init__.py` - Package initialization for tests
- `backend/tests/test_main.py` - Tests for main FastAPI application
- `backend/tests/test_routers/` - Tests for router endpoints
- `backend/tests/test_agents/` - Tests for agent implementations
- `backend/tests/test_ingestion/` - Tests for ingestion pipeline
- `backend/requirements.txt` - Python dependencies
- `backend/.env` - Backend environment variables
- `backend/.gitignore` - Git ignore rules

### Notes

- All frontend files follow Next.js 14.x App Router structure with TypeScript
- All backend files follow FastAPI naming conventions with Python 3.11+:
  - API routes are in `routers/` folder (not `api/`)
  - Pydantic schemas are in `schemas/` folder (plural, not `schema/`)
  - All package directories include `__init__.py` files
  - Shared dependencies are in `dependencies.py`
  - Tests are in `tests/` folder at root level
- LangChain v1.0 patterns are used throughout (create_agent, supervisor pattern, @tool decorator)
- Unit tests for backend should be placed in `backend/tests/` folder following FastAPI conventions
- Frontend unit tests should be placed alongside code files (e.g., `Component.test.tsx`)
- Use `npm test` for frontend tests and `pytest` for backend tests

---

## Tasks

- [ ] 1.0 Build Frontend Application (Next.js)
  - [ ] 1.1 Initialize Next.js 14.x project with TypeScript, App Router, and TailwindCSS
  - [ ] 1.2 Set up project structure: create `src/app/`, `src/components/`, `src/layouts/`, `src/context/`, `src/hooks/`, `src/services/`, `src/utils/`, `src/constants/`, `src/styles/`, and `public/` folders
  - [ ] 1.3 Install and configure dependencies: Next.js, React, shadcn/ui, TailwindCSS, TypeScript, and required UI libraries
  - [ ] 1.4 Create `next.config.js`, `tsconfig.json`, and `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`
  - [ ] 1.5 Create `src/constants/api-endpoints.ts` with API endpoint URLs (chat, upload, collections, sessions, feedback, health)
  - [ ] 1.6 Create `src/utils/file-handlers.ts` with file validation utilities (format, size, corruption checks)
  - [ ] 1.7 Create `src/utils/stream-parser.ts` with SSE stream parsing utilities
  - [ ] 1.8 Create `src/services/api-client.ts` with API client functions for backend communication (POST, GET, DELETE, SSE streaming)
  - [ ] 1.9 Create `src/styles/globals.css` with TailwindCSS setup and aerospace-themed color palette (blues, grays)
  - [ ] 1.10 Create `src/layouts/Header.tsx` with title "The Aerospace Company Customer Service Agent" and airplane logo icon prominently displayed
  - [ ] 1.11 Create `src/context/ChatContext.tsx` with chat state management (messages, streaming status, session ID)
  - [ ] 1.12 Create `src/context/SessionContext.tsx` with session management (session list, active session, history)
  - [ ] 1.13 Create `src/hooks/useChat.ts` custom hook for chat functionality with SSE streaming support
  - [ ] 1.14 Create `src/hooks/useUpload.ts` custom hook for document upload with progress tracking
  - [ ] 1.15 Create `src/hooks/useSession.ts` custom hook for session management (create, list, switch, delete)
  - [ ] 1.16 Create `src/components/ChatInterface/MessageList.tsx` with scrollable container showing conversation history with clear visual distinction between user and AI messages
  - [ ] 1.17 Create `src/components/ChatInterface/InputBox.tsx` with multi-line text input field and "Send" button
  - [ ] 1.18 Create `src/components/ChatInterface/StreamingResponse.tsx` to handle and display SSE streaming tokens in real-time
  - [ ] 1.19 Create `src/components/ChatInterface/SatisfactionFeedback.tsx` with thumbs up/down buttons, optional feedback text box, and submit functionality
  - [ ] 1.20 Create `src/components/DocumentUpload/FileUploader.tsx` with drag-and-drop file picker supporting multiple file selection
  - [ ] 1.21 Create `src/components/DocumentUpload/FilePreview.tsx` to preview selected files with names, sizes, and remove buttons
  - [ ] 1.22 Create `src/components/DocumentUpload/KnowledgeBaseSelector.tsx` dropdown populated from `/collections` endpoint with "Auto-Map" as default option
  - [ ] 1.23 Create `src/components/DocumentUpload/UploadProgress.tsx` to display upload progress (percentage and file-by-file status)
  - [ ] 1.24 Create `src/app/page.tsx` main chat interface page integrating MessageList, InputBox, StreamingResponse, and SatisfactionFeedback components
  - [ ] 1.25 Create `src/app/upload/page.tsx` document upload page integrating FileUploader, FilePreview, KnowledgeBaseSelector, and UploadProgress components
  - [ ] 1.26 Add airplane logo icon to `public/` folder and configure static asset serving
  - [ ] 1.27 Implement responsive design for desktop browsers (Chrome, Firefox, Safari, Edge) with minimum viewport support of 1024x768
  - [ ] 1.28 Add accessibility features: keyboard navigation, ARIA labels, and WCAG AA color contrast compliance
  - [ ] 1.29 Test frontend application: verify all components render correctly and basic navigation works

- [ ] 2.0 Set Up ChromaDB Data Layer with Three Knowledge Base Collections
  - [ ] 2.1 Create `backend/app/__init__.py` package initialization file
  - [ ] 2.2 Create `backend/app/utils/__init__.py` package initialization file
  - [ ] 2.3 Create `backend/app/utils/config.py` with environment variable loading using python-dotenv (OPENAI_API_KEY, AWS credentials, etc.)
  - [ ] 2.4 Create `backend/app/utils/logger.py` with logging configuration
  - [ ] 2.5 Create `backend/app/retrieval/__init__.py` package initialization file
  - [ ] 2.6 Create `backend/app/retrieval/chroma_client.py` with ChromaDB client initialization using local persistence (`./chroma_db` directory)
  - [ ] 2.7 Implement function to create or get three separate ChromaDB collections: `billing_knowledge_base`, `technical_knowledge_base`, `policy_knowledge_base`
  - [ ] 2.8 Configure ChromaDB with OpenAI embeddings (text-embedding-3-small, 1536 dimensions) for all collections
  - [ ] 2.9 Implement collection metadata management (source file name, upload timestamp, document category, chunk index)
  - [ ] 2.10 Create `backend/app/main.py` FastAPI application entry point with basic CORS setup and health endpoint
  - [ ] 2.11 Create `backend/app/routers/__init__.py` package initialization file
  - [ ] 2.12 Create `backend/app/routers/health.py` with GET /health endpoint that checks ChromaDB connectivity
  - [ ] 2.13 Create `backend/app/routers/collections.py` with GET /collections endpoint returning list of available knowledge base collections
  - [ ] 2.14 Create `backend/requirements.txt` with initial dependencies: FastAPI, Uvicorn, ChromaDB, python-dotenv, OpenAI
  - [ ] 2.15 Test ChromaDB setup: verify three collections are created successfully and can be queried

- [ ] 3.0 Build Document Ingestion Pipeline
  - [ ] 3.1 Create `backend/app/ingestion/__init__.py` package initialization file
  - [ ] 3.2 Create `backend/app/ingestion/parsers/__init__.py` package initialization file
  - [ ] 3.3 Create `backend/app/ingestion/parsers/pdf_parser.py` using PyPDFLoader from LangChain to parse PDF documents
  - [ ] 3.4 Create `backend/app/ingestion/parsers/txt_parser.py` using TextLoader from LangChain to parse plain text documents
  - [ ] 3.5 Create `backend/app/ingestion/parsers/markdown_parser.py` using UnstructuredMarkdownLoader from LangChain to parse Markdown documents
  - [ ] 3.6 Create `backend/app/ingestion/parsers/json_parser.py` using JSON loader to parse JSON documents
  - [ ] 3.7 Create parser factory function that selects appropriate parser based on file extension
  - [ ] 3.8 Create `backend/app/ingestion/chunkers/__init__.py` package initialization file
  - [ ] 3.9 Create `backend/app/ingestion/chunkers/recursive_chunker.py` using RecursiveCharacterTextSplitter from LangChain with chunk_size=1000 and chunk_overlap=200
  - [ ] 3.10 Create `backend/app/ingestion/embeddings/__init__.py` package initialization file
  - [ ] 3.11 Create `backend/app/ingestion/embeddings/openai_embedder.py` using OpenAIEmbeddings (model: text-embedding-3-small, 1536 dimensions)
  - [ ] 3.12 Create `backend/app/ingestion/ingest_data.py` main ingestion pipeline that: accepts file path and target collection, parses document, chunks text, generates embeddings, stores vectors in ChromaDB with metadata
  - [ ] 3.13 Implement Auto-Map categorization logic: analyze document content to determine appropriate knowledge base (billing, technical, or policy) based on keywords and content analysis
  - [ ] 3.14 Implement file validation: check file format (PDF, TXT, Markdown, JSON), size (target: average 100 KB, max per file validation), and corruption before processing
  - [ ] 3.15 Add metadata enrichment: include source file name, upload timestamp, document category, and chunk index in ChromaDB documents
  - [ ] 3.16 Implement error handling: handle parsing errors, embedding generation failures, and ChromaDB storage errors gracefully
  - [ ] 3.17 Test ingestion pipeline: verify PDF, TXT, Markdown, and JSON files are processed correctly and stored in appropriate collections

- [ ] 4.0 Connect Frontend Upload Interface to Backend Ingestion Pipeline
  - [ ] 4.1 Create `backend/app/schemas/__init__.py` package initialization file
  - [ ] 4.2 Create `backend/app/schemas/upload.py` with Pydantic schemas for upload requests (files, target_collection) and responses (upload_id, status, files, progress)
  - [ ] 4.3 Create `backend/app/routers/upload.py` with POST /upload endpoint that: accepts multipart file uploads, validates files, queues ingestion tasks asynchronously, returns upload_id and status
  - [ ] 4.4 Implement file validation in upload endpoint: check format (PDF, TXT, Markdown, JSON), size limits, and file corruption
  - [ ] 4.5 Implement Auto-Map logic: if "Auto-Map" is selected, analyze document content to determine target collection; if specific collection is selected, use that collection
  - [ ] 4.6 Integrate ingestion pipeline with upload endpoint: call `ingest_data.py` for each uploaded file asynchronously
  - [ ] 4.7 Implement upload progress tracking: maintain upload status (queued, processing, completed, failed) and percentage complete for each file
  - [ ] 4.8 Create `backend/app/routers/collections.py` GET /collections endpoint that returns list of available knowledge base collections from ChromaDB
  - [ ] 4.9 Update `frontend/src/hooks/useUpload.ts` to call POST /upload endpoint and handle multipart form data with file uploads
  - [ ] 4.10 Update `frontend/src/hooks/useUpload.ts` to poll for upload progress or implement SSE for real-time progress updates
  - [ ] 4.11 Update `frontend/src/components/DocumentUpload/KnowledgeBaseSelector.tsx` to fetch collections from GET /collections endpoint and populate dropdown
  - [ ] 4.12 Update `frontend/src/components/DocumentUpload/FileUploader.tsx` to integrate with useUpload hook and handle file selection
  - [ ] 4.13 Update `frontend/src/components/DocumentUpload/UploadProgress.tsx` to display progress from upload status
  - [ ] 4.14 Update `frontend/src/components/DocumentUpload/FilePreview.tsx` to display selected files and allow removal before upload
  - [ ] 4.15 Implement error handling: display success/error notifications for each upload attempt with appropriate error messages
  - [ ] 4.16 Test end-to-end upload flow: verify files upload successfully, are processed, and stored in correct ChromaDB collections

- [x] 5.0 Build Supervisor Agent (Orchestrator) ✅ **COMPLETE - 100% TEST PASS RATE**
  - [x] 5.1 Create `backend/app/agents/__init__.py` package initialization file
  - [x] 5.2 Create `backend/app/schemas/chat.py` with Pydantic schemas for chat requests (session_id, message, stream) and responses
  - [x] 5.3 Create `backend/app/state/__init__.py` package initialization file
  - [x] 5.4 Create `backend/app/state/conversation_state.py` with InMemorySaver from langgraph.checkpoint.memory for conversation persistence
  - [x] 5.5 Create `backend/app/agents/orchestrator.py` with supervisor agent implementation using `create_agent()` from langchain.agents
  - [x] 5.6 Configure supervisor agent: use AWS Bedrock model ("bedrock:claude-3-haiku" or similar), provide descriptive name ("supervisor_agent"), include system prompt emphasizing query routing to appropriate worker tools
  - [x] 5.7 Create placeholder worker agent tool functions (billing_tool, technical_tool, policy_tool) using `@tool` decorator that will be connected to actual worker agents later
  - [x] 5.8 Configure tool descriptions for supervisor routing: billing_tool ("Handle billing inquiries, pricing questions, contract terms, invoices"), technical_tool ("Handle technical questions, component specifications, bug reports, technical manuals"), policy_tool ("Handle regulatory compliance questions, FAA/EASA regulations, policy inquiries")
  - [x] 5.9 Create emergency detection tool `detect_emergency(query: str) -> str` using `@tool` decorator that analyzes query for safety-critical keywords and returns escalation message with contact information (john.doe@aerospace-co.com) if emergency detected
  - [x] 5.10 Add emergency detection tool and placeholder worker tools (billing_tool, technical_tool, policy_tool) to supervisor agent's tools list
  - [x] 5.11 Configure supervisor agent with InMemorySaver() checkpointer for conversation persistence
  - [x] 5.12 Implement supervisor agent invocation pattern: accept query and session_id (thread_id), invoke agent with config={"configurable": {"thread_id": session_id}}
  - [x] 5.13 Update `backend/app/routers/chat.py` with POST /chat endpoint that: accepts chat message and session_id, invokes supervisor agent, streams response using Server-Sent Events (SSE), returns agent metadata
  - [x] 5.14 Implement SSE streaming in chat endpoint: stream tokens from supervisor agent to frontend in real-time
  - [x] 5.15 Implement session management: generate unique session_id (thread_id) for new conversations, maintain session context across browser refreshes
  - [x] 5.16 Test supervisor agent: verified agent can be invoked and returns responses (32 tests, 100% pass rate)

- [x] 6.0 Build Policy & Compliance Agent (Pure CAG) ✅ **COMPLETE - 100% TEST PASS RATE**
  - [x] 6.1 Create `backend/app/retrieval/cag_retriever.py` with Pure CAG retrieval implementation (no vector retrieval, uses static policy documents)
  - [x] 6.2 Implement CAG retrieval tool: create `@tool` decorated function `search_policy_kb(query: str) -> str` that queries policy_knowledge_base ChromaDB collection and returns formatted context (for now, use simple text matching or predefined responses until full CAG is implemented)
  - [x] 6.3 Create `backend/app/agents/policy_agent.py` with Policy & Compliance Agent using `create_agent()` from langchain.agents
  - [x] 6.4 Configure policy agent: use OpenAI model ("openai:gpt-4o-mini"), provide descriptive name ("policy_compliance_agent"), include system prompt emphasizing: domain expertise in FAA/EASA regulations, DFARs policies, data governance, customer support policies; CRITICAL instruction to include ALL results and details in final response; source citation requirements
  - [x] 6.5 Add CAG retrieval tool to policy agent's tools list
  - [x] 6.6 Configure policy agent with InMemorySaver() checkpointer for conversation persistence
  - [x] 6.7 Create `policy_tool` wrapper function using `@tool` decorator that: accepts request string, invokes policy_agent.invoke() with query, returns final message content from agent response
  - [x] 6.8 Update supervisor agent in `backend/app/agents/orchestrator.py` to replace placeholder policy_tool with actual policy_tool implementation
  - [x] 6.9 Test policy agent independently: verified agent can be invoked, uses CAG retrieval, and returns responses with source citations (26 tests, 100% pass rate)
  - [x] 6.10 Test policy agent through supervisor: verified supervisor can route policy-related queries to policy agent and receive responses

- [x] 7.0 Build Technical Support Agent (Pure RAG) ✅ **COMPLETE - 100% TEST PASS RATE**
  - [x] 7.1 Create `backend/app/retrieval/rag_retriever.py` with Pure RAG retrieval implementation
  - [x] 7.2 Implement RAG retrieval tool: create `@tool` decorated function `search_technical_kb(query: str) -> str` that queries technical_knowledge_base ChromaDB collection using similarity_search (k=3), retrieves top documents, and returns formatted context with document names and excerpts
  - [x] 7.3 Create `backend/app/agents/technical_agent.py` with Technical Support Agent using `create_agent()` from langchain.agents
  - [x] 7.4 Configure technical agent: use OpenAI model ("openai:gpt-4o-mini"), provide descriptive name ("technical_support_agent"), include system prompt emphasizing: domain expertise in technical documentation, bug reports, specifications; CRITICAL instruction to include ALL results and details in final response; source citation requirements
  - [x] 7.5 Add RAG retrieval tool to technical agent's tools list
  - [x] 7.6 Configure technical agent with InMemorySaver() checkpointer for conversation persistence
  - [x] 7.7 Create `technical_tool` wrapper function using `@tool` decorator that: accepts request string, invokes technical_agent.invoke() with query, returns final message content from agent response
  - [x] 7.8 Update supervisor agent in `backend/app/agents/orchestrator.py` to replace placeholder technical_tool with actual technical_tool implementation
  - [x] 7.9 Test technical agent independently: verify agent can be invoked, uses RAG retrieval to query ChromaDB, and returns responses with source citations (26 tests, 100% pass rate)
  - [x] 7.10 Test technical agent through supervisor: verified supervisor can route technical-related queries to technical agent and receive responses

- [x] 8.0 Build Billing Support Agent (Hybrid RAG/CAG) ✅ **COMPLETE - 100% TEST PASS RATE**
  - [x] 8.1 Create `backend/app/retrieval/hybrid_retriever.py` with Hybrid RAG/CAG retrieval implementation
  - [x] 8.2 Implement Hybrid RAG/CAG strategy: initial queries use RAG to retrieve dynamic information from billing_knowledge_base, static policy information is cached in session memory after first retrieval, subsequent queries in same session use cached policy data when applicable
  - [x] 8.3 Implement RAG retrieval tool for billing: create `@tool` decorated function `search_billing_kb(query: str) -> str` that queries billing_knowledge_base ChromaDB collection using similarity_search (k=3) and returns formatted context
  - [x] 8.4 Implement CAG caching logic: create mechanism to cache static policy information in session memory after first RAG retrieval, check cache before performing RAG retrieval for subsequent queries
  - [x] 8.5 Create `backend/app/agents/billing_agent.py` with Billing Support Agent using `create_agent()` from langchain.agents
  - [x] 8.6 Configure billing agent: use OpenAI model ("openai:gpt-4o-mini"), provide descriptive name ("billing_support_agent"), include system prompt emphasizing: domain expertise in billing, pricing, contracts, invoices; CRITICAL instruction to include ALL results and details in final response; source citation requirements; instructions to use cached policy data when appropriate
  - [x] 8.7 Add both RAG retrieval tool and CAG caching logic to billing agent's tools list
  - [x] 8.8 Configure billing agent with InMemorySaver() checkpointer for conversation persistence
  - [x] 8.9 Create `billing_tool` wrapper function using `@tool` decorator that: accepts request string, invokes billing_agent.invoke() with query, returns final message content from agent response
  - [x] 8.10 Update supervisor agent in `backend/app/agents/orchestrator.py` to replace placeholder billing_tool with actual billing_tool implementation
  - [x] 8.11 Test billing agent independently: verify agent can be invoked, uses Hybrid RAG/CAG (initial RAG query, subsequent cached queries), and returns responses with source citations (28 tests, 100% pass rate)
  - [x] 8.12 Test billing agent through supervisor: verified supervisor can route billing-related queries to billing agent and receive responses
  - [x] 8.13 Test complete multi-agent system: verified supervisor correctly routes queries to all three agents (Policy, Technical, Billing) based on query intent (8 tests, 100% pass rate)

