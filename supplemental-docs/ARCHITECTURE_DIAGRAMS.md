# Advanced Customer Service AI - Architecture Diagrams (Mermaid)

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph UI[Frontend Layer - Next.js]
        Chat[Chat Interface]
        Upload[Document Upload UI]
        Session[Session Manager]
        History[Conversation History]
    end
    
    subgraph API[API Gateway - FastAPI]
        ChatEP[/chat endpoint]
        UploadEP[/upload endpoint]
        SessionEP[/sessions endpoint]
        HealthEP[/health endpoint]
    end
    
    subgraph Agent[Agentic Middleware - LangGraph]
        Orchestrator[Orchestrator Agent - Supervisor/Router]
        BillingAgent[Billing Agent - Hybrid RAG/CAG]
        TechAgent[Technical Agent - Pure RAG]
        PolicyAgent[Policy Agent - Pure CAG]
    end
    
    subgraph Data[Data Layer]
        ChromaDB[ChromaDB Vector Database]
        BillingKB[Billing KB - Hybrid Store]
        TechKB[Technical KB - RAG Store]
        PolicyKB[Policy KB - CAG Store]
    end
    
    subgraph LLM[LLM Providers]
        OpenAI[OpenAI GPT-4 - High Quality]
        Bedrock[AWS Bedrock Claude Haiku - Cost-Effective]
    end
    
    subgraph Ingest[Ingestion Pipeline]
        Parser[Document Parser - PDF/TXT/MD/JSON]
        Chunker[Chunking Engine]
        Embedder[Embedding Generator - OpenAI]
        Storer[Vector Storage]
    end
    
    Chat -->|POST /chat| ChatEP
    Upload -->|POST /upload| UploadEP
    Session -->|GET/POST /sessions| SessionEP
    History -->|GET /history| SessionEP
    
    ChatEP --> Orchestrator
    UploadEP --> Ingest
    SessionEP --> Agent
    HealthEP --> LLM
    
    Orchestrator -->|Route Query| BillingAgent
    Orchestrator -->|Route Query| TechAgent
    Orchestrator -->|Route Query| PolicyAgent
    
    BillingAgent --> ChromaDB
    TechAgent --> ChromaDB
    PolicyAgent --> ChromaDB
    
    ChromaDB --> BillingKB
    ChromaDB --> TechKB
    ChromaDB --> PolicyKB
    
    BillingAgent -->|Query| OpenAI
    TechAgent -->|Query| OpenAI
    PolicyAgent -->|Query| Bedrock
    
    Parser --> Chunker
    Chunker --> Embedder
    Embedder --> Storer
    Storer --> ChromaDB
    
    style UI fill:#e1f5ff
    style API fill:#fff3e0
    style Agent fill:#f3e5f5
    style Data fill:#e8f5e9
    style LLM fill:#fce4ec
    style Ingest fill:#fff9c4
```

---

## 2. Frontend Component Architecture

```mermaid
graph TB
    subgraph Pages[Pages Layer]
        IndexPage[index.tsx - Chat]
        UploadPage[upload.tsx - Document Upload]
        DashPage[dashboard.tsx - Sessions]
    end
    
    subgraph Components[Components Layer]
        direction TB
        subgraph Chat[Chat Components]
            MsgList[MessageList.tsx]
            InputBox[InputBox.tsx]
            StreamResp[StreamingResponse.tsx]
        end
        
        subgraph Upload[Upload Components]
            FileUp[FileUploader.tsx]
            FilePreview[FilePreview.tsx]
            UploadProg[UploadProgress.tsx]
            UploadHist[UploadHistory.tsx]
        end
        
        subgraph Session[Session Components]
            Sidebar[HistorySidebar.tsx]
            SessionList[SessionList.tsx]
            ClearHist[ClearHistory.tsx]
        end
        
        subgraph Common[Common Components]
            Header[Header.tsx]
            NavBar[Sidebar.tsx]
            Footer[Footer.tsx]
        end
    end
    
    subgraph Hooks[Custom Hooks]
        UseChat[useChat.ts]
        UseUpload[useUpload.ts]
        UseSession[useSession.ts]
    end
    
    subgraph Utils[Utilities]
        APIClient[api-client.ts]
        FileHandlers[file-handlers.ts]
        StreamParser[stream-parser.ts]
    end
    
    IndexPage --> Chat
    UploadPage --> Upload
    DashPage --> Session
    
    Chat --> UseChat
    Upload --> UseUpload
    Session --> UseSession
    
    UseChat --> APIClient
    UseUpload --> APIClient
    UseSession --> APIClient
    
    APIClient --> FileHandlers
    APIClient --> StreamParser
    
    style Pages fill:#bbdefb
    style Chat fill:#c8e6c9
    style Upload fill:#ffe0b2
    style Session fill:#f8bbd0
    style Common fill:#e1bee7
    style Hooks fill:#b2dfdb
    style Utils fill:#fff9c4
```

---

## 3. Backend Module Architecture

```mermaid
graph TB
    Main[main.py - FastAPI App]
    
    subgraph API[API Routes]
        ChatRoute[chat.py - POST /chat]
        UploadRoute[upload.py - POST /upload]
        SessionRoute[sessions.py - CRUD /sessions]
        HealthRoute[health.py - GET /health]
    end
    
    subgraph Agents[Agents Module]
        OrchestratorAgent[orchestrator.py - Supervisor]
        BillingAgentImpl[billing_agent.py - Hybrid RAG/CAG]
        TechAgentImpl[technical_agent.py - Pure RAG]
        PolicyAgentImpl[policy_agent.py - Pure CAG]
    end
    
    subgraph Retrieval[Retrieval Module]
        ChromaClient[chroma_client.py - DB Connection]
        RAGRetriever[rag_retriever.py - Vector Search]
        CAGRetriever[cag_retriever.py - LLM Generation]
        HybridRetriever[hybrid_retriever.py - RAG + CAG]
    end
    
    subgraph Ingestion[Ingestion Module]
        IngestMain[ingest_data.py - Main Pipeline]
        
        subgraph Parsers[Parsers]
            PDFParser[pdf_parser.py]
            TXTParser[txt_parser.py]
            MDParser[markdown_parser.py]
            JSONParser[json_parser.py]
        end
        
        subgraph Chunkers[Chunkers]
            RecursiveChunker[recursive_chunker.py]
            SemanticChunker[semantic_chunker.py]
            FixedChunker[fixed_size_chunker.py]
        end
        
        Embeddings[openai_embedder.py]
    end
    
    subgraph LLMLayer[LLM Layer]
        OpenAIClient[openai_client.py - GPT-4]
        BedrockClient[bedrock_client.py - Claude Haiku]
        LLMRouter[llm_router.py - Provider Selection]
    end
    
    subgraph Schema[Schema Module]
        ChatSchema[chat.py - Message, Request, Response]
        UploadSchema[upload.py - Upload Request/Response]
        SessionSchema[session.py - Session, History]
    end
    
    subgraph State[State Module]
        ConvState[conversation_state.py - LangGraph State]
    end
    
    subgraph Utils[Utilities]
        Logger[logger.py]
        Config[config.py]
    end
    
    Main --> API
    Main --> Agents
    
    ChatRoute --> OrchestratorAgent
    UploadRoute --> IngestMain
    SessionRoute --> ConvState
    HealthRoute --> LLMRouter
    
    OrchestratorAgent --> BillingAgentImpl
    OrchestratorAgent --> TechAgentImpl
    OrchestratorAgent --> PolicyAgentImpl
    
    BillingAgentImpl --> HybridRetriever
    TechAgentImpl --> RAGRetriever
    PolicyAgentImpl --> CAGRetriever
    
    HybridRetriever --> ChromaClient
    RAGRetriever --> ChromaClient
    CAGRetriever --> ChromaClient
    
    HybridRetriever --> LLMRouter
    RAGRetriever --> LLMRouter
    CAGRetriever --> LLMRouter
    
    LLMRouter --> OpenAIClient
    LLMRouter --> BedrockClient
    
    IngestMain --> Parsers
    IngestMain --> Chunkers
    Chunkers --> Embeddings
    Embeddings --> ChromaClient
    
    Agents --> Schema
    API --> Schema
    
    Logger --> Utils
    Config --> Utils
    
    style API fill:#fff3e0
    style Agents fill:#f3e5f5
    style Retrieval fill:#e8f5e9
    style Ingestion fill:#fff9c4
    style LLMLayer fill:#fce4ec
    style Schema fill:#e0f2f1
    style State fill:#ede7f6
```

---

## 4. LangGraph Agent Orchestration Flow

```mermaid
stateDiagram-v2
    [*] --> InputValidation
    
    InputValidation --> Orchestrator: Query validated
    
    Orchestrator --> RoutingDecision
    
    state RoutingDecision <<choice>>
    RoutingDecision --> BillingAgent: Billing Query
    RoutingDecision --> TechAgent: Technical Query
    RoutingDecision --> PolicyAgent: Policy Query
    
    BillingAgent --> RetrieveBilling
    state RetrieveBilling {
        [*] --> QueryDB: Hybrid RAG/CAG
        QueryDB --> [*]: Context Retrieved
    }
    RetrieveBilling --> GenerateResponse
    
    TechAgent --> RetrieveTech
    state RetrieveTech {
        [*] --> QueryDB2: Pure RAG
        QueryDB2 --> [*]: Context Retrieved
    }
    RetrieveTech --> GenerateResponse
    
    PolicyAgent --> RetrievePolicy
    state RetrievePolicy {
        [*] --> QueryDB3: Pure CAG
        QueryDB3 --> [*]: Context Retrieved
    }
    RetrievePolicy --> GenerateResponse
    
    GenerateResponse --> LLMCall
    
    state LLMCall <<choice>>
    LLMCall --> OpenAIGPT4: Complex Query
    LLMCall --> ClaudeHaiku: Simple/Routing
    
    OpenAIGPT4 --> Format
    ClaudeHaiku --> Format
    
    state Format {
        [*] --> Structure: Format Response
        Structure --> Citations: Add Citations
        Citations --> Metadata: Include Metadata
        Metadata --> [*]
    }
    
    Format --> Stream
    Stream --> SaveHistory
    SaveHistory --> [*]
```

---

## 5. Document Ingestion Pipeline

```mermaid
flowchart LR
    subgraph Input[Input Stage]
        User[User Selects Multiple Files]
        Frontend[Frontend Upload UI]
    end
    
    subgraph Processing[Processing Stage]
        Validation[File Validation]
        Parsing[Document Parsing]
        Chunking[Chunking Engine]
    end
    
    subgraph Generation[Generation Stage]
        Embedding[Embedding Generation]
        Metadata[Metadata Enrichment]
    end
    
    subgraph Storage[Storage Stage]
        Routing[Route to Collection]
        ChromaStore[Store in ChromaDB]
        Verification[Verification]
    end
    
    Output[Ingestion Complete]
    
    User --> Frontend
    Frontend --> Validation
    Validation --> Parsing
    Parsing --> Chunking
    Chunking --> Embedding
    Embedding --> Metadata
    Metadata --> Routing
    Routing --> ChromaStore
    ChromaStore --> Verification
    Verification --> Output
    
    style Input fill:#e3f2fd
    style Processing fill:#f3e5f5
    style Generation fill:#fce4ec
    style Storage fill:#e8f5e9
    style Output fill:#c8e6c9
```

---

## 6. Chat Query Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant LangGraph
    participant ChromaDB
    participant LLM
    
    User->>Frontend: Types message
    Frontend->>Backend: POST /chat (stream: true)
    Backend->>Backend: Extract message & session
    Backend->>LangGraph: Add to input state
    
    LangGraph->>LangGraph: Input Validation
    LangGraph->>LangGraph: Orchestrator analyzes query
    
    alt Billing Query
        LangGraph->>LangGraph: Route to Billing Agent
        LangGraph->>ChromaDB: Query billing_knowledge_base
    else Technical Query
        LangGraph->>LangGraph: Route to Technical Agent
        LangGraph->>ChromaDB: Query technical_knowledge_base
    else Policy Query
        LangGraph->>LangGraph: Route to Policy Agent
        LangGraph->>ChromaDB: Query policy_knowledge_base
    end
    
    ChromaDB-->>LangGraph: Return relevant documents
    LangGraph->>LangGraph: Apply retrieval strategy
    
    LangGraph->>LLM: Request response generation
    LLM-->>LangGraph: Stream response tokens
    
    LangGraph->>Backend: Stream formatted tokens
    Backend-->>Frontend: SSE stream (token by token)
    Frontend->>Frontend: Render streaming response
    Frontend-->>User: Display in real-time
    
    LangGraph->>Backend: Save to conversation history
    Backend->>Backend: Store session & messages
```

---

## 7. Document Upload Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Queue
    participant Pipeline
    participant ChromaDB
    
    User->>Frontend: Select multiple files
    Frontend->>Frontend: File validation & preview
    User->>Frontend: Click upload
    
    Frontend->>Backend: POST /upload (multipart)
    Backend->>Backend: Validate files
    Backend->>Backend: Store temporarily
    Backend->>Queue: Queue ingestion tasks
    Backend-->>Frontend: 202 Accepted (upload_id)
    
    Frontend->>Frontend: Show progress UI
    
    Note over Queue,ChromaDB: Background Processing
    Queue->>Pipeline: Start processing
    
    Pipeline->>Pipeline: Parse PDF/TXT/MD/JSON
    Pipeline->>Pipeline: Chunk documents
    Pipeline->>Pipeline: Generate embeddings
    
    Pipeline->>Pipeline: Detect category
    alt Billing Documents
        Pipeline->>ChromaDB: Store in billing_kb
    else Technical Documents
        Pipeline->>ChromaDB: Store in technical_kb
    else Policy Documents
        Pipeline->>ChromaDB: Store in policy_kb
    end
    
    Pipeline->>Pipeline: Verify storage
    Pipeline->>Backend: Update upload status
    
    Frontend->>Backend: GET /upload/status/{upload_id}
    Backend-->>Frontend: progress: 45%
    Frontend->>Frontend: Update progress bar
    
    loop Every 2 seconds
        Frontend->>Backend: Poll status
        Backend-->>Frontend: Updated progress
    end
    
    Backend-->>Frontend: status: completed
    Frontend->>Frontend: Show success message
    Frontend-->>User: Documents ready for RAG!
```

---

## 8. Vector Database Collections

```mermaid
graph TB
    subgraph ChromaDB[ChromaDB Vector Database]
        subgraph BillingKB[billing_knowledge_base]
            B1[Doc: billing_001]
            B2[Doc: billing_002]
            B3[Doc: ...]
        end
        
        subgraph TechKB[technical_knowledge_base]
            T1[Doc: tech_001]
            T2[Doc: tech_002]
            T3[Doc: ...]
        end
        
        subgraph PolicyKB[policy_knowledge_base]
            P1[Doc: policy_001]
            P2[Doc: policy_002]
            P3[Doc: ...]
        end
        
        Storage[SQLite Backend with Vector Index]
    end
    
    BillingAgent[Billing Agent - Hybrid RAG/CAG]
    TechAgent[Technical Agent - Pure RAG]
    PolicyAgent[Policy Agent - Pure CAG]
    
    BillingAgent -.Query.-> BillingKB
    TechAgent -.Query.-> TechKB
    PolicyAgent -.Query.-> PolicyKB
    
    BillingKB --> Storage
    TechKB --> Storage
    PolicyKB --> Storage
    
    style ChromaDB fill:#e8f5e9
    style BillingKB fill:#fff9c4
    style TechKB fill:#c8e6c9
    style PolicyKB fill:#bbdefb
```

---

## 9. Retrieval Strategy Comparison

```mermaid
graph TB
    Query[User Query]
    
    Query --> RAG[RAG Strategy]
    Query --> CAG[CAG Strategy]
    Query --> Hybrid[Hybrid Strategy]
    
    RAG --> RAGStep1[1. Retrieve from Vector DB]
    RAGStep1 --> RAGStep2[2. Generate with context]
    RAGStep2 --> RAGOutput[Output: Fresh context-aware responses]
    
    CAG --> CAGStep1[1. Use cached knowledge]
    CAGStep1 --> CAGStep2[2. Generate consistently]
    CAGStep2 --> CAGOutput[Output: Fast consistent responses]
    
    Hybrid --> HybridStep1[1. Retrieve dynamic content]
    HybridStep1 --> HybridStep2[2. Cache static info]
    HybridStep2 --> HybridStep3[3. Generate optimally]
    HybridStep3 --> HybridOutput[Output: Balanced efficient responses]
    
    RAGOutput --> Use1[Use Case: Technical Support]
    CAGOutput --> Use2[Use Case: Policy Questions]
    HybridOutput --> Use3[Use Case: Billing Support]
    
    style RAG fill:#c8e6c9
    style CAG fill:#fff9c4
    style Hybrid fill:#ffe0b2
    style Use1 fill:#bbdefb
    style Use2 fill:#f8bbd0
    style Use3 fill:#e1bee7
```

---

## 10. LLM Provider Selection Strategy

```mermaid
graph TD
    Query[Incoming Query]
    
    Query --> Orchestrator[Orchestrator Agent - Supervisor]
    
    Orchestrator --> Decision{Query Complexity?}
    
    Decision -->|Simple Routing| Bedrock[AWS Bedrock Claude 3 Haiku]
    Decision -->|Complex Query| OpenAI[OpenAI GPT-4]
    
    Bedrock --> BedrockFeatures[Fast responses<br/>Cost-effective<br/>Good for routing]
    OpenAI --> OpenAIFeatures[High quality<br/>Multi-step reasoning<br/>Better accuracy]
    
    BedrockFeatures --> Response1[Response - Routed to agent]
    OpenAIFeatures --> Response2[Response - Final answer]
    
    Response1 --> Frontend[Frontend - Stream to user]
    Response2 --> Frontend
    
    style Orchestrator fill:#f3e5f5
    style Bedrock fill:#fff9c4
    style OpenAI fill:#fce4ec
    style Frontend fill:#e1f5ff
```

---

## 11. API Endpoints Architecture

```mermaid
graph TB
    API[FastAPI Application]
    
    API --> Chat[Chat Endpoints]
    API --> Upload[Upload Endpoints]
    API --> Session[Session Endpoints]
    API --> Health[Health Endpoints]
    
    Chat --> PostChat[POST /chat]
    Chat --> GetHistory[GET /history/session_id]
    
    Upload --> PostUpload[POST /upload]
    Upload --> GetUploadStatus[GET /upload/status/upload_id]
    Upload --> GetUploadHistory[GET /upload/history]
    
    Session --> PostSession[POST /sessions]
    Session --> GetSessions[GET /sessions]
    Session --> GetSessionById[GET /sessions/session_id]
    Session --> PutSession[PUT /sessions/session_id]
    Session --> DeleteSession[DELETE /sessions/session_id]
    
    Health --> GetHealth[GET /health]
    Health --> GetStatus[GET /status]
    
    style Chat fill:#bbdefb
    style Upload fill:#fff9c4
    style Session fill:#c8e6c9
    style Health fill:#f8bbd0
```

---

## 12. Complete System Integration

```mermaid
graph TB
    subgraph Frontend[Frontend - Next.js + React]
        UI[User Interface<br/>Chat, Upload, Sessions]
    end
    
    subgraph Backend[Backend - FastAPI]
        API[API Routes<br/>chat, upload, sessions, health]
    end
    
    subgraph Orchestration[Orchestration - LangGraph]
        Supervisor[Supervisor Agent]
        Workers[Worker Agents<br/>Billing, Technical, Policy]
    end
    
    subgraph Retrieval[Retrieval Strategies]
        RAG[RAG Retriever]
        CAG[CAG Retriever]
        Hybrid[Hybrid Retriever]
    end
    
    subgraph Data[Data & Knowledge]
        Vectors[Vector DB - ChromaDB]
        Collections[3 Collections<br/>Billing, Technical, Policy]
    end
    
    subgraph LLMs[LLM Providers]
        OpenAI[OpenAI GPT-4]
        Bedrock[AWS Bedrock Claude]
    end
    
    subgraph Ingestion[Ingestion Pipeline]
        Parser[Document Parser]
        Chunker[Chunking Engine]
        Embedder[Embedding Generator]
    end
    
    Frontend -->|HTTP/WebSocket| Backend
    Backend --> API
    
    API -->|Query| Orchestration
    API -->|Upload| Ingestion
    
    Supervisor -->|Route| Workers
    
    Workers -->|Retrieve| Retrieval
    
    RAG --> Vectors
    CAG --> Vectors
    Hybrid --> Vectors
    
    Vectors --> Collections
    
    Workers -->|Generate| LLMs
    
    OpenAI -->|Response| Workers
    Bedrock -->|Response| Workers
    
    Ingestion --> Parser
    Parser --> Chunker
    Chunker --> Embedder
    Embedder --> Vectors
    
    Workers -->|Stream| Backend
    Backend -->|SSE| Frontend
    
    style Frontend fill:#e1f5ff
    style Backend fill:#fff3e0
    style Orchestration fill:#f3e5f5
    style Retrieval fill:#e8f5e9
    style Data fill:#ede7f6
    style LLMs fill:#fce4ec
    style Ingestion fill:#fff9c4
```

---

## Summary of Diagrams

| # | Diagram | Type | Purpose |
|---|---------|------|---------|
| 1 | High-Level System | Graph | Complete system overview with all major components |
| 2 | Frontend Architecture | Graph | Next.js component structure and organization |
| 3 | Backend Architecture | Graph | FastAPI modules and layer organization |
| 4 | LangGraph Flow | State Diagram | Agent orchestration and state machine |
| 5 | Ingestion Pipeline | Flowchart | Document processing workflow |
| 6 | Chat Query Flow | Sequence | User query processing interaction |
| 7 | Upload Flow | Sequence | Document upload interaction |
| 8 | Vector DB Collections | Graph | ChromaDB structure and organization |
| 9 | Retrieval Strategies | Graph | Comparison of RAG vs CAG vs Hybrid |
| 10 | LLM Selection | Graph | Provider selection logic |
| 11 | API Endpoints | Graph | All API endpoints organized by category |
| 12 | System Integration | Graph | Complete integrated system overview |

---

## Notes on Rendering

These Mermaid diagrams are compatible with:
- ✅ **GitHub** - Renders automatically in markdown files
- ✅ **GitLab** - Native Mermaid support
- ✅ **Mermaid Live Editor** - https://mermaid.live
- ✅ **VS Code** - With Mermaid Preview extension
- ✅ **Notion** - Use Mermaid embed blocks
- ✅ **Confluence** - With Mermaid plugin

If you encounter rendering issues on a specific platform, try:
1. Removing emojis from subgraph labels
2. Simplifying node labels
3. Using the Mermaid Live Editor to test and debug
