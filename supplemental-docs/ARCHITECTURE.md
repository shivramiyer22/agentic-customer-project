# Advanced Customer Service AI - Application Architecture

## System Overview

This document outlines the complete architecture of the multi-agent customer service AI system, including the frontend, backend, agentic middleware, and data ingestion pipeline.

---

## 1. High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            USER INTERFACE LAYER                              │
│                                (Frontend)                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      Next.js React Application                        │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │   │
│  │  │  Chat Interface  │  │ Document Upload  │  │ Session Manager  │   │   │
│  │  │  - Messages      │  │ - Multiple files │  │ - History        │   │   │
│  │  │  - Real-time     │  │ - File preview   │  │ - Context        │   │   │
│  │  │  - Streaming     │  │ - Upload status  │  │ - Settings       │   │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────────────────┘
                           │
                    HTTP/WebSocket
                           │
┌──────────────────────────▼──────────────────────────────────────────────────┐
│                         API GATEWAY LAYER                                    │
│                        (FastAPI Backend)                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        FastAPI Server                                │   │
│  │  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────┐  │   │
│  │  │ /chat (Streaming)  │  │ /upload (Documents)│  │ /health      │  │   │
│  │  │ POST Request       │  │ POST Multipart     │  │ GET Status   │  │   │
│  │  └────────────────────┘  └────────────────────┘  └──────────────┘  │   │
│  │  ┌────────────────────┐  ┌────────────────────┐                     │   │
│  │  │ /history           │  │ /sessions          │                     │   │
│  │  │ GET Conversation   │  │ GET/DELETE Session │                     │   │
│  │  └────────────────────┘  └────────────────────┘                     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼────────┐  ┌─────▼──────────┐
│  Ingestion   │  │ Agent Query     │  │ Retrieval      │
│  Endpoint    │  │ Orchestration   │  │ Coordination   │
└───────┬──────┘  └────────┬────────┘  └─────┬──────────┘
        │                  │                  │
┌───────▼──────────────────▼──────────────────▼──────────────┐
│             AGENTIC MIDDLEWARE LAYER                       │
│                  (LangGraph Framework)                     │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Orchestrator Agent (Supervisor)            │   │
│  │  - Analyzes incoming query                         │   │
│  │  - Routes to appropriate worker agent              │   │
│  │  - Manages conversation state                      │   │
│  │  - Maintains session context & history             │   │
│  └────┬─────────────────┬─────────────────┬───────────┘   │
│       │                 │                 │                │
│  ┌────▼──────────┐ ┌────▼──────────┐ ┌───▼─────────────┐ │
│  │ Billing Agent │ │ Technical     │ │ Policy &        │ │
│  │               │ │ Support Agent │ │ Compliance      │ │
│  │ Strategy:     │ │               │ │ Agent           │ │
│  │ Hybrid        │ │ Strategy:     │ │                 │ │
│  │ RAG/CAG       │ │ Pure RAG      │ │ Strategy:       │ │
│  │ - Dynamic     │ │ - Dynamic KB  │ │ Pure CAG        │ │
│  │   Q&A         │ │ - Tech docs   │ │ - Static docs   │ │
│  │ - Policy      │ │ - Bug reports │ │ - ToS, Privacy  │ │
│  │   caching     │ │ - Forum posts │ │ - Consistency   │ │
│  └────┬──────────┘ └────┬──────────┘ └───┬─────────────┘ │
│       │                 │                 │                │
│       └─────────────────┼─────────────────┘                │
│                         │                                  │
└─────────────────────────┼──────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────────┐ ┌────▼────────┐ ┌─────▼─────────┐
│ Retrieval Layer  │ │ LLM Layer   │ │ Ingestion     │
│ (Vector DBs)     │ │ (Providers) │ │ Pipeline      │
└───────┬──────────┘ └────┬────────┘ └─────┬─────────┘
        │                 │                │
│
├─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│                                                             │
│  ┌──────────────────────┐      ┌──────────────────────┐   │
│  │    ChromaDB Vector   │      │  LLM Providers       │   │
│  │    Database Stores   │      │                      │   │
│  │                      │      │  ┌────────────────┐  │   │
│  │  ┌────────────────┐  │      │  │ OpenAI (GPT-4) │  │   │
│  │  │ Billing KB     │  │      │  │ High quality   │  │   │
│  │  │ (Hybrid Store) │  │      │  │ responses      │  │   │
│  │  └────────────────┘  │      │  └────────────────┘  │   │
│  │                      │      │                      │   │
│  │  ┌────────────────┐  │      │  ┌────────────────┐  │   │
│  │  │ Technical KB   │  │      │  │ AWS Bedrock    │  │   │
│  │  │ (RAG Store)    │  │      │  │ (Claude Haiku) │  │   │
│  │  └────────────────┘  │      │  │ Cost-effective │  │   │
│  │                      │      │  │ routing        │  │   │
│  │  ┌────────────────┐  │      │  └────────────────┘  │   │
│  │  │ Policy KB      │  │      │                      │   │
│  │  │ (CAG Store)    │  │      │                      │   │
│  │  └────────────────┘  │      │                      │   │
│  └──────────────────────┘      └──────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │     Document Ingestion Pipeline (ingest_data.py)    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │ Document     │  │ Chunking &   │  │ Vector     │ │  │
│  │  │ Processing   │  │ Embedding    │  │ Storage in │ │  │
│  │  │ - PDF        │  │ Generation   │  │ ChromaDB   │ │  │
│  │  │ - TXT        │──│ - OpenAI     │──│ Stores     │ │  │
│  │  │ - Markdown   │  │   Embeddings │  │            │ │  │
│  │  │ - JSON       │  │              │  │            │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Frontend Architecture (Next.js)

```
Next.js Application
├── pages/
│   ├── api/
│   │   └── proxy/ (API request forwarding)
│   ├── index.tsx (Main chat page)
│   ├── upload.tsx (Document upload page)
│   └── dashboard.tsx (Session management)
├── components/
│   ├── ChatInterface/
│   │   ├── MessageList.tsx
│   │   ├── InputBox.tsx
│   │   └── StreamingResponse.tsx
│   ├── DocumentUpload/
│   │   ├── FileUploader.tsx
│   │   ├── FilePreview.tsx
│   │   ├── UploadProgress.tsx
│   │   └── UploadHistory.tsx
│   ├── SessionManager/
│   │   ├── HistorySidebar.tsx
│   │   ├── SessionList.tsx
│   │   └── ClearHistory.tsx
│   └── common/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── Footer.tsx
├── hooks/
│   ├── useChat.ts
│   ├── useUpload.ts
│   └── useSession.ts
├── utils/
│   ├── api-client.ts
│   ├── file-handlers.ts
│   └── stream-parser.ts
└── styles/
    └── globals.css (shadcn/ui theme)
```

---

## 3. Backend Architecture (FastAPI)

```
FastAPI Application
├── main.py
│   ├── FastAPI app initialization
│   ├── CORS setup
│   ├── Route registration
│   └── Exception handlers
├── api/
│   ├── __init__.py
│   ├── chat.py
│   │   ├── POST /chat (stream responses)
│   │   └── Message schema validation
│   ├── upload.py
│   │   ├── POST /upload (handle file uploads)
│   │   ├── File validation
│   │   └── Queue to ingestion pipeline
│   ├── sessions.py
│   │   ├── GET /sessions (list user sessions)
│   │   ├── POST /sessions (create session)
│   │   ├── GET /sessions/{id} (get session history)
│   │   └── DELETE /sessions/{id} (delete session)
│   └── health.py
│       └── GET /health (service status)
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   │   ├── Supervisor Agent
│   │   ├── Query routing logic
│   │   └── State management
│   ├── billing_agent.py
│   │   ├── Hybrid RAG/CAG strategy
│   │   ├── Billing KB retrieval
│   │   └── Policy caching
│   ├── technical_agent.py
│   │   ├── Pure RAG strategy
│   │   ├── Technical KB retrieval
│   │   └── Dynamic knowledge base
│   └── policy_agent.py
│       ├── Pure CAG strategy
│       ├── Static policy retrieval
│       └── Consistency management
├── retrieval/
│   ├── __init__.py
│   ├── chroma_client.py
│   │   ├── ChromaDB initialization
│   │   └── Collection management
│   ├── rag_retriever.py
│   │   ├── Vector similarity search
│   │   ├── Context retrieval
│   │   └── Hybrid search
│   ├── cag_retriever.py
│   │   ├── LLM-based generation
│   │   ├── Template-based generation
│   │   └── Consistency checker
│   └── hybrid_retriever.py
│       ├── RAG + CAG fusion
│       └── Adaptive routing
├── ingestion/
│   ├── __init__.py
│   ├── ingest_data.py (main pipeline)
│   │   ├── File processor
│   │   ├── Document parser
│   │   ├── Chunking strategy
│   │   ├── Embedding generation
│   │   ├── ChromaDB storage
│   │   └── Error handling
│   ├── parsers/
│   │   ├── pdf_parser.py
│   │   ├── txt_parser.py
│   │   ├── markdown_parser.py
│   │   └── json_parser.py
│   ├── chunkers/
│   │   ├── recursive_chunker.py
│   │   ├── semantic_chunker.py
│   │   └── fixed_size_chunker.py
│   └── embeddings/
│       └── openai_embedder.py
├── llm/
│   ├── __init__.py
│   ├── openai_client.py
│   │   └── GPT-4 integration
│   ├── bedrock_client.py
│   │   └── Claude Haiku integration
│   └── llm_router.py
│       ├── Provider selection
│       └── Cost optimization
├── schema/
│   ├── __init__.py
│   ├── chat.py
│   │   ├── ChatMessage
│   │   ├── ChatRequest
│   │   └── ChatResponse
│   ├── upload.py
│   │   ├── UploadRequest
│   │   └── UploadResponse
│   └── session.py
│       ├── Session
│       └── SessionHistory
├── state/
│   ├── __init__.py
│   └── conversation_state.py
│       ├── Message history
│       ├── Session context
│       └── Agent memory
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── config.py
└── requirements.txt
```

---

## 4. Agentic Middleware Architecture (LangGraph)

```
LangGraph Agent Orchestration

State Schema:
├── messages: List[BaseMessage]
├── session_id: str
├── user_query: str
├── routing_decision: str
├── context: Dict
├── retrieved_docs: List[Document]
├── final_response: str
└── metadata: Dict

Graph Flow:
┌─────────────────┐
│  START: Query   │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│  Input Validation        │
│  - Sanitize query        │
│  - Extract intent        │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Orchestrator Agent      │
│  (Supervisor/Router)     │
│  - Analyze query         │
│  - Determine category    │
│  - Route to agent        │
└────┬───┬───┬─────────────┘
     │   │   │
     │   │   └─────────────────┐
     │   └──────────┐          │
     │              │          │
     ▼              ▼          ▼
┌─────────────┐ ┌──────────┐ ┌──────────────┐
│ Billing     │ │Technical │ │Policy &      │
│ Agent       │ │Support   │ │Compliance    │
│             │ │Agent     │ │Agent         │
│ Retrieval:  │ │          │ │              │
│ Hybrid      │ │Retrieval:│ │Retrieval:    │
│ RAG/CAG     │ │Pure RAG  │ │Pure CAG      │
└─────┬───────┘ └─────┬────┘ └──────┬───────┘
      │               │             │
      ▼               ▼             ▼
┌─────────────────────────────────────────────┐
│  Retrieve Context/Generate Response         │
│  - Query vector DB                          │
│  - Apply retrieval strategy                 │
│  - Generate response with LLM               │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌──────────────────────────┐
│  Response Formatting     │
│  - Structure response    │
│  - Add citations        │
│  - Include metadata     │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│  Stream to Frontend      │
│  - Real-time SSE        │
│  - Message tokens       │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│  Save to History         │
│  - Store in memory       │
│  - Update session state  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│  END: Response Complete  │
└──────────────────────────┘
```

---

## 5. Vector Database Architecture (ChromaDB)

```
ChromaDB Persistence Layer

Collections:
├── billing_knowledge_base
│   ├── Document ID: "billing_001"
│   ├── Content: "Pricing information..."
│   ├── Embeddings: [0.1, 0.2, 0.3, ...]
│   ├── Metadata: {
│   │   "source": "pricing_guide.pdf",
│   │   "category": "billing",
│   │   "timestamp": "2024-01-15"
│   │}
│   └── Storage Type: Hybrid (for RAG + CAG)
│
├── technical_knowledge_base
│   ├── Document ID: "tech_001"
│   ├── Content: "API documentation..."
│   ├── Embeddings: [0.2, 0.3, 0.4, ...]
│   ├── Metadata: {
│   │   "source": "api_docs.md",
│   │   "category": "technical",
│   │   "timestamp": "2024-01-15"
│   │}
│   └── Storage Type: RAG optimized
│
└── policy_knowledge_base
    ├── Document ID: "policy_001"
    ├── Content: "Terms of Service..."
    ├── Embeddings: [0.3, 0.4, 0.5, ...]
    ├── Metadata: {
    │   "source": "tos.pdf",
    │   "category": "policy",
    │   "timestamp": "2024-01-15"
    │}
    └── Storage Type: CAG optimized
```

---

## 6. Document Ingestion Pipeline Flow

```
User Upload Flow:

1. Frontend (Document Upload UI)
   ├── User selects multiple files
   ├── File validation (type, size)
   ├── Preview generation
   └── Submit to /upload endpoint

2. FastAPI Backend (/upload)
   ├── Receive multipart form data
   ├── Temporary file storage
   ├── Queue ingestion tasks
   └── Return upload confirmation

3. Ingestion Pipeline (ingest_data.py)
   ├── Document Processing
   │  ├── PDF parser (pypdf, pdfplumber)
   │  ├── TXT parser (plain text)
   │  ├── Markdown parser
   │  └── JSON parser
   │
   ├── Chunking Strategy
   │  ├── Recursive character chunking
   │  ├── Chunk overlap: 20%
   │  └── Target chunk size: 1000 tokens
   │
   ├── Embedding Generation
   │  ├── OpenAI Embeddings API
   │  ├── Model: text-embedding-3-small
   │  └── Dimension: 1536
   │
   ├── Metadata Enrichment
   │  ├── Source file name
   │  ├── Upload timestamp
   │  ├── Document category
   │  └── Chunk index
   │
   ├── Vector Storage
   │  ├── Determine target collection
   │  │  ├── Billing docs → billing_knowledge_base
   │  │  ├── Tech docs → technical_knowledge_base
   │  │  └── Policy docs → policy_knowledge_base
   │  └── Store vectors with metadata
   │
   └── Verification
      ├── Count stored embeddings
      ├── Validate retrieval
      └── Log ingestion metrics

4. Persistent Storage (ChromaDB)
   ├── Local SQLite backend
   ├── Vector index
   └── Metadata storage
```

---

## 7. LLM Provider Strategy

```
Provider Selection Logic:

┌──────────────────────────────────┐
│    Query Orchestrator            │
└────────────┬─────────────────────┘
             │
             ▼
    ┌────────────────────────┐
    │  Routing Decision      │
    │  (Supervisor Agent)    │
    └────┬───┬───────────────┘
         │   │
         │   └──────────────────────────┐
         │                              │
    ┌────▼─────────────────┐   ┌────────▼──────────────┐
    │ Complex Query        │   │ Simple Query/Routing │
    │ High-quality needed  │   │ Cost-sensitive       │
    │                      │   │                      │
    │ Use: OpenAI (GPT-4)  │   │ Use: AWS Bedrock     │
    │ - Detailed analysis  │   │      (Claude Haiku)  │
    │ - Multi-step reason  │   │ - Fast responses     │
    │ - Better accuracy    │   │ - Cost-effective     │
    │ - For final response │   │ - For routing logic  │
    └────────────────────┘    └─────────────────────┘
```

---

## 8. API Endpoints Reference

```
Authentication (if needed):
├── POST /auth/login → JWT Token
└── POST /auth/logout → Invalidate Token

Chat Endpoints:
├── POST /chat
│   ├── Request: { "session_id": str, "message": str, "stream": bool }
│   ├── Response: EventStream or { "response": str, "metadata": {} }
│   └── Streaming: Server-Sent Events (SSE)
│
└── GET /history/{session_id}
    ├── Response: { "messages": [Message], "metadata": {} }
    └── Status: 200 OK or 404 Not Found

Document Upload Endpoints:
├── POST /upload
│   ├── Request: multipart/form-data { files: [File], category?: str }
│   ├── Response: { "upload_id": str, "status": "queued", "files": [...] }
│   └── Status: 202 Accepted (async processing)
│
├── GET /upload/status/{upload_id}
│   ├── Response: { "status": "processing|completed|failed", "progress": % }
│   └── Status: 200 OK
│
└── GET /upload/history
    ├── Response: { "uploads": [UploadRecord] }
    └── Status: 200 OK

Session Management Endpoints:
├── POST /sessions
│   ├── Request: { "title": str, "tags": [str] }
│   ├── Response: { "session_id": str, "created_at": timestamp }
│   └── Status: 201 Created
│
├── GET /sessions
│   ├── Response: { "sessions": [Session], "total": int }
│   └── Status: 200 OK
│
├── GET /sessions/{session_id}
│   ├── Response: { "session_id": str, "history": [Message], "metadata": {} }
│   └── Status: 200 OK
│
├── PUT /sessions/{session_id}
│   ├── Request: { "title": str, "tags": [str] }
│   ├── Response: { "session_id": str, "updated_at": timestamp }
│   └── Status: 200 OK
│
└── DELETE /sessions/{session_id}
    ├── Response: { "message": "Session deleted" }
    └── Status: 204 No Content

Health & Status Endpoints:
├── GET /health
│   ├── Response: { "status": "healthy", "timestamp": timestamp }
│   └── Status: 200 OK
│
└── GET /status
    ├── Response: { "service": "active", "chroma_db": "connected", "llm": "ready" }
    └── Status: 200 OK
```

---

## 9. Data Flow Diagram

```
User Query Flow:

Frontend                      Backend                    Agentic Layer              LLM & Data
   │                            │                            │                        │
   ├─ User types message        │                            │                        │
   ├─ Clicks send              │                            │                        │
   │                            │                            │                        │
   ├─ POST /chat ──────────────▶│                            │                        │
   │   (stream: true)           │                            │                        │
   │                            │ ─ Extract message          │                        │
   │                            │ ─ Create session if new    │                        │
   │                            │                            │                        │
   │                            ├─ Add to LangGraph ────────▶│                        │
   │                            │   input state              │                        │
   │                            │                            │ ─ Orchestrator analyzes│
   │                            │                            │   query category       │
   │                            │                            │                        │
   │                            │                            ├─ Routes to agent ────▶│
   │                            │                            │   (Billing/Tech/Policy)│
   │                            │                            │                        │
   │                            │                            │ ─ Apply retrieval:     │
   │                            │                            │   - Query ChromaDB     │
   │                            │                            │   - Get embeddings    │
   │                            │                            ├──────────────────────▶│
   │                            │                            │   Retrieve context     │
   │                            │                            │   (RAG/CAG/Hybrid)     │
   │                            │                            │                        │
   │                            │                            │   Generate response    │
   │                            │                            │ ◀──────────────────────┤
   │                            │                            │ (LLM provider)         │
   │                            │                            │                        │
   │                            │◀──── Stream tokens ────────┤                        │
   │◀─ SSE stream ────────────│                            │                        │
   │   (token by token)        │                            │                        │
   │                            │ ─ Save to history          │                        │
   │                            │                            │                        │
   ├─ Display message           │                            │                        │
   │   in real-time             │                            │                        │
   │                            │                            │                        │


Document Upload Flow:

Frontend                      Backend                    Ingestion Pipeline          ChromaDB
   │                            │                            │                        │
   ├─ User selects files       │                            │                        │
   ├─ File preview shows       │                            │                        │
   ├─ Clicks upload            │                            │                        │
   │                            │                            │                        │
   ├─ POST /upload ───────────▶│                            │                        │
   │   (multipart form)         │                            │                        │
   │                            │ ─ Validate files          │
   │                            │ ─ Store temporarily       │
   │                            │                            │
   │                            ├─ Queue ingestion ────────▶│                        │
   │                            │   (background task)        │                        │
   │                            │                            │                        │
   │◀─ 202 Accepted ───────────┤                            │                        │
   │   (upload_id)              │                            │                        │
   │                            │                            │                        │
   ├─ Poll progress            │                            │                        │
   ├─ GET /upload/status       │                            │                        │
   │                            │ ─ Return progress         │                        │
   │◀─ { "progress": 45% }     │                            │                        │
   │                            │                            │                        │
   │                            │                            │ ─ Parse PDF/TXT/etc    │
   │                            │                            │ ─ Chunk documents      │
   │                            │                            │ ─ Generate embeddings  │
   │                            │                            │                        │
   │                            │                            ├─ Store vectors ──────▶│
   │                            │                            │   in collection        │
   │                            │                            │                        │
   │◀─ 100% Complete ─────────┤                            │   Done!               │
```

---

## 10. Implementation Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Next.js | 14.x | React framework, SSR/SSG |
| | React | 18.x | UI components |
| | shadcn/ui | Latest | UI component library |
| | TailwindCSS | 3.x | Styling |
| | Axios | 1.x | HTTP client |
| **Backend** | Python | 3.11+ | Server language |
| | FastAPI | 0.100+ | Web framework |
| | Uvicorn | 0.23+ | ASGI server |
| | Pydantic | 2.x | Data validation |
| **Agentic** | LangChain | 0.1+ | LLM framework |
| | LangGraph | Latest | Agent orchestration |
| | LCEL | Latest | Expression language |
| **AI/LLM** | OpenAI | Latest API | GPT-4 for quality responses |
| | AWS Bedrock | Latest | Claude Haiku for routing |
| **Data** | ChromaDB | 0.4+ | Vector database |
| | Pandas | 2.x | Data manipulation |
| **Document Processing** | pypdf | 3.x | PDF parsing |
| | pdfplumber | 0.10+ | Advanced PDF extraction |
| | python-docx | 0.8.11 | DOCX support |
| **Utilities** | Pydantic | 2.x | Serialization |
| | python-dotenv | Latest | Environment config |
| | Celery (optional) | 5.x | Async task queue |

---

## 11. Key Design Patterns

### 11.1 Agent Routing Pattern
- **Supervisor Agent** analyzes query intent
- Routes to specialized worker agents based on category
- Each agent has optimized retrieval strategy

### 11.2 Retrieval Strategy Pattern
- **RAG (Retrieval-Augmented Generation)**: Retrieve then generate
- **CAG (Cached Augmented Generation)**: Cache + generate
- **Hybrid**: Combine both for optimal performance

### 11.3 State Management
- LangGraph manages conversation state
- Maintains message history
- Preserves session context across turns

### 11.4 Streaming Response Pattern
- FastAPI Server-Sent Events (SSE)
- Frontend streams tokens in real-time
- Better UX with visible generation progress

---

## 12. Deployment Considerations

```
Development:
├── Backend: localhost:8000
├── Frontend: localhost:3000
└── ChromaDB: Local persistence

Production:
├── Backend: Docker container (AWS/GCP/Azure)
├── Frontend: Vercel or similar (CDN)
├── ChromaDB: Managed service or persistent volume
├── LLM APIs: Configure with production credentials
└── Document Storage: S3 or similar for uploaded files
```

---

## Summary

This architecture provides:
- ✅ **Scalable** multi-agent system with LangGraph orchestration
- ✅ **Flexible** retrieval strategies (RAG/CAG/Hybrid)
- ✅ **Cost-optimized** LLM provider selection
- ✅ **User-friendly** document upload interface
- ✅ **Persistent** vector database with ChromaDB
- ✅ **Real-time** streaming responses
- ✅ **Session management** for conversation context
- ✅ **Production-ready** with error handling and logging


