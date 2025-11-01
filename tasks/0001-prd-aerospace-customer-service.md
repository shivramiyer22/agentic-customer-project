# Product Requirements Document: Aerospace Customer Service AI System

**Version:** 1.0  
**Date:** November 1, 2025  
**Status:** Draft  
**Document ID:** 0001-prd-aerospace-customer-service

---

## 1. Introduction/Overview

### Problem Statement

Internal customer service representatives at The Aerospace Company face significant challenges when handling customer inquiries:

1. **Slow Response Times:** Representatives must manually search through multiple knowledge sources (technical manuals, billing documents, regulatory policies) to find accurate answers, leading to long wait times for customers.

2. **Inconsistent Information:** Different representatives may provide varying answers to similar questions, especially for complex topics involving billing, technical specifications, or regulatory compliance.

3. **Resource Constraints:** Scaling customer service operations requires hiring more representatives, increasing costs without proportionally improving service quality.

4. **Knowledge Management:** Representatives struggle to stay current with frequently updated documents, including FAA/EASA regulations, technical service bulletins, parts catalogs, and policy changes.

### Solution

This PRD defines a sophisticated, proof-of-concept multi-agent AI system built with LangChain v1.0 that assists internal customer service representatives by intelligently routing customer inquiries to specialized AI agents. The system uses a **supervisor pattern** where an orchestrator agent coordinates specialized worker agents (Billing Support, Technical Support, Policy & Compliance) as tools.

Each agent is optimized with a specific retrieval strategy:
- **Billing Support Agent:** Hybrid RAG/CAG for dynamic pricing queries and cached policy information
- **Technical Support Agent:** Pure RAG for dynamic technical documentation and bug reports
- **Policy & Compliance Agent:** Pure CAG for consistent, fast responses from static regulatory documents

The system provides real-time streaming responses, maintains conversation history, and includes emergency escalation for safety-critical queries.

### Goal

Enable internal customer service representatives to deliver faster (target: <30 seconds), more accurate, and consistent responses to customer inquiries across billing, technical, and policy domains, while reducing the need for manual research and improving overall customer satisfaction.

---

## 2. Goals

1. **Enable Representatives to Deliver Faster, More Accurate Responses:** Reduce research time for representatives from minutes to seconds by automatically retrieving relevant information from specialized knowledge bases.

2. **Improve Response Accuracy and Consistency:** Ensure all representatives receive the same high-quality, source-backed answers regardless of their individual knowledge or experience level.

3. **Scale Customer Service Operations:** Support increased inquiry volume without proportionally increasing headcount by empowering existing representatives with AI assistance.

4. **Demonstrate Advanced AI Architecture:** Showcase a production-ready multi-agent system using LangChain v1.0 supervisor pattern with diverse retrieval strategies (RAG, CAG, Hybrid).

5. **Empower Representatives:** Provide representatives with a tool that enhances their capabilities, reduces cognitive load, and enables them to focus on complex problem-solving and customer relationship building.

6. **Maintain High Representative Satisfaction:** Achieve and maintain at least 80% thumbs up rating from representatives through accurate, timely, and helpful AI-assisted responses.

---

## 3. User Stories

### Internal Customer Service Representative Stories

**US-1:** As a customer service representative, I want to input a technical question about a component specification and receive an accurate, source-backed answer so that I can quickly respond to my customer's inquiry without manual research.

**US-2:** As a customer service representative, I want the system to automatically route my query to the appropriate specialized agent (Billing, Technical, or Policy) so that I receive the most relevant response without needing to understand the system's internal routing logic.

**US-3:** As a customer service representative, I want to quickly access billing information including parts pricing, contract terms, and invoice details so that I can resolve billing-related customer inquiries efficiently.

**US-4:** As a customer service representative, I want to see source citations for all information provided by the AI so that I can verify accuracy and build trust with customers.

**US-5:** As a customer service representative, I want the system to maintain conversation history within a session so that I can reference previous exchanges and provide contextual responses in ongoing conversations.

**US-6:** As a customer service representative, I want to upload new documents to the knowledge base so that the system stays current with the latest technical manuals, regulations, and policy updates.

**US-7:** As a customer service representative, I want to manually select which knowledge base (Billing, Technical, or Policy) a document should be uploaded to, or use Auto-Map for automatic categorization, so that documents are stored in the correct collection.

**US-8:** As a customer service representative, I want to receive real-time streaming responses so that I can see the AI's response as it generates, improving my sense of system responsiveness and allowing me to prepare follow-up questions.

**US-12:** As a customer service representative, at the end of each conversation, I want to provide quick feedback using thumbs up or thumbs down buttons, with an optional text box for additional comments, so that I can easily rate the quality of AI assistance and help improve the system.

### Team Lead/Management Stories

**US-9:** As a team lead, I want to review conversation histories to understand common inquiry patterns and representative needs so that I can identify training opportunities and improve team performance.

**US-10:** As a team lead, I want to see usage metrics and satisfaction scores so that I can measure adoption rates, ROI, and the system's impact on customer satisfaction.

### Critical Safety Story

**US-11:** As a customer service representative, when I receive an emergency or safety-critical query (e.g., "aircraft emergency", "in-flight failure", "safety incident"), I want the system to immediately detect this and provide clear escalation instructions with contact information (**ski@aerospace-co.com**) so that critical safety issues are routed to appropriate personnel without delay.

---

## 4. Functional Requirements

### 4.1 Core Chat Functionality

**FR-1:** The system must provide a web-based chat interface where representatives can submit text-based customer inquiries.

**FR-2:** The system must display conversation history showing both representative queries and AI responses in chronological order.

**FR-3:** The system must support real-time streaming of AI responses using Server-Sent Events (SSE) so that representatives see tokens as they are generated.

**FR-4:** The system must indicate which specialized agent (Billing Support, Technical Support, or Policy & Compliance) generated each response, displayed clearly in the UI.

**FR-5:** The system must include source citations with all AI responses, displaying document names and relevant excerpts that support the answer.

### 4.2 Multi-Agent Orchestration

**FR-6:** The system must implement a **supervisor agent** using LangChain v1.0 tool calling pattern that analyzes incoming queries and routes them to appropriate worker agents.

**FR-7:** The system must create three specialized worker agents using `create_agent()` from `langchain.agents`:
   - Billing Support Agent
   - Technical Support Agent  
   - Policy & Compliance Agent

**FR-8:** Each specialized worker agent must be wrapped as a tool using the `@tool` decorator, allowing the supervisor to invoke them through tool calls.

**FR-9:** The supervisor agent must use tool descriptions to determine which worker agent to invoke based on query intent and content.

**FR-10:** The system must visually indicate which agent generated each response by parsing tool execution results from the supervisor agent.

**FR-11:** Worker agents must include all information, findings, and details in their final response messages, as the supervisor agent only sees the final output from each worker (not intermediate reasoning or tool calls).

### 4.3 Retrieval Strategies

**FR-12:** The Billing Support Agent must implement a **Hybrid RAG/CAG strategy**:
   - Initial queries use RAG to retrieve dynamic information from the billing knowledge base
   - Static policy information is cached in session memory after first retrieval
   - Subsequent queries in the same session use cached policy data when applicable

**FR-13:** The Technical Support Agent must implement a **Pure RAG strategy**, retrieving information from a dynamic knowledge base of technical documents, bug reports, and forum posts.

**FR-14:** The Policy & Compliance Agent must implement a **Pure CAG strategy**, providing fast, consistent answers from static policy documents without vector retrieval for each query.

**FR-15:** All retrieval strategies must query the appropriate ChromaDB collection based on the agent's knowledge domain.

### 4.4 Document Ingestion

**FR-16:** The system must provide a document upload interface with a dropdown menu listing all available knowledge base collections (billing_knowledge_base, technical_knowledge_base, policy_knowledge_base), plus an "Auto-Map" option.

**FR-17:** The system must support uploading documents in the following formats: PDF, TXT, Markdown (.md), and JSON.

**FR-18:** When "Auto-Map" is selected (default option), the system must automatically analyze uploaded documents and categorize them into the appropriate knowledge base collection (billing, technical, or policy) based on content analysis.

**FR-19:** When a specific knowledge base is manually selected from the dropdown, all uploaded documents must be stored in that selected collection, regardless of content.

**FR-20:** The system must process uploaded documents through a pipeline that:
   - Parses documents using appropriate loaders (PyPDFLoader, TextLoader, UnstructuredMarkdownLoader)
   - Splits documents into chunks using RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=200)
   - Generates embeddings using OpenAI embeddings API (model: text-embedding-3-small)
   - Stores vectors and metadata in the appropriate ChromaDB collection

**FR-21:** The system must display upload progress (percentage complete) and final status (success/failure) for each uploaded file.

**FR-22:** The system must validate uploaded files for format, size (target: average 100 KB per file, up to 100 files per collection), and corruption before processing.

### 4.5 Knowledge Base Mappings

**FR-23:** The **billing_knowledge_base** collection must store documents related to:
   - Parts catalogs with pricing information
   - Contract documents and terms
   - Invoice templates and billing procedures
   - Pricing policies and rate cards

**FR-24:** The **technical_knowledge_base** collection must store documents related to:
   - Bug reports and issue tracking documents
   - Technical manuals and specifications
   - Engineering specifications and technical publications
   - Technical service bulletins

**FR-25:** The **policy_knowledge_base** collection must store documents related to:
   - FAA and EASA regulatory documents
   - Government policies and DFARs (Defense Federal Acquisition Regulation Supplement)
   - Data governance policies
   - Customer support policies (incidence/bug reporting procedures, service levels, ageing policies)
   - Invoicing policies for both US Government defense contracts and commercial businesses

### 4.6 Emergency Escalation

**FR-26:** The system must detect safety-critical or emergency queries using keyword and intent analysis (e.g., "emergency", "aircraft failure", "safety incident", "in-flight").

**FR-27:** When an emergency query is detected, the system must immediately display a prominent escalation notice with clear instructions and contact information: **ski@aerospace-co.com**.

**FR-28:** The system must log all emergency escalations with timestamp, query content, and representative session ID for audit purposes.

**FR-29:** The system must continue to attempt providing an AI response alongside the escalation notice, as representatives may still benefit from relevant information while waiting for human assistance.

### 4.7 Session Management

**FR-30:** The system must persist conversation history for each session using `InMemorySaver()` from `langgraph.checkpoint.memory`, storing only the last 3 chat conversations per representative following a FIFO (First In, First Out) retention policy.

**FR-31:** The system must generate a unique session ID (thread_id) for each new conversation and maintain session context across browser refreshes.

**FR-32:** The system must maintain session context across browser refreshes by passing a consistent `thread_id` in the config when invoking agents.

**FR-33:** Representatives must be able to view and switch between their last 3 historical conversations.

**FR-34:** The system must display conversation timestamps and allow representatives to clear individual conversations.

### 4.8 LLM Provider Strategy

**FR-35:** The system must use **OpenAI (GPT-4o-mini)** for generating high-quality final responses from specialized worker agents.

**FR-36:** The system must use **AWS Bedrock (Claude 3 Haiku or Nova Lite)** for fast, cost-effective query routing and classification in the supervisor agent.

**FR-37:** The system must optimize LLM usage by using cheaper models (Bedrock) for frequent operations (routing) and premium models (OpenAI) for final customer-facing responses.

### 4.9 Vector Database

**FR-38:** The system must use ChromaDB with local persistence for all vector storage, maintaining three separate collections:
   - billing_knowledge_base
   - technical_knowledge_base
   - policy_knowledge_base

**FR-39:** The system must use OpenAI embeddings (text-embedding-3-small, 1536 dimensions) for all vector generation.

**FR-40:** The system must implement similarity search with configurable parameters (default: k=3 documents per query).

**FR-41:** The system must store document metadata including source file name, upload timestamp, document category, and chunk index.

**FR-42:** The system must handle approximately 100 files per knowledge base collection, with average file size of 100 KB, totaling approximately 10 MB per collection.

### 4.10 API Endpoints

**FR-43:** The system must provide a `POST /chat` endpoint that accepts a chat message and session ID, streams responses using Server-Sent Events (SSE), and returns agent metadata.

**FR-44:** The system must provide a `POST /upload` endpoint that accepts multipart file uploads, processes documents asynchronously, and returns upload status with progress tracking.

**FR-45:** The system must provide a `GET /collections` endpoint that returns a list of all available knowledge base collections from ChromaDB for populating the upload interface dropdown.

**FR-46:** The system must provide a `GET /sessions` endpoint that returns a list of the representative's last 3 conversations (FIFO).

**FR-47:** The system must provide a `GET /sessions/{session_id}` endpoint that returns the full conversation history for a specific session.

**FR-48:** The system must provide a `DELETE /sessions/{session_id}` endpoint that allows representatives to delete individual conversation histories.

**FR-49:** The system must provide a `GET /health` endpoint that returns system status including ChromaDB connectivity and LLM provider availability.

**FR-50:** The system must provide a `POST /feedback` endpoint that accepts satisfaction feedback:
   - Request body: `{ "session_id": str, "rating": "thumbs_up" | "thumbs_down", "comment": str | null }`
   - Response: `{ "success": bool, "message": str }`
   - Status: 200 OK on success, 400 Bad Request for invalid data

### 4.11 User Interface

**FR-51:** The frontend application must be titled **"The Aerospace Company Customer Service Agent"** with this title prominently displayed in the header.

**FR-52:** The header must include an airplane logo icon to reinforce the aerospace branding.

**FR-53:** The chat interface must display messages in a scrollable container with clear visual distinction between representative queries and AI responses.

**FR-54:** The chat interface must include a text input field at the bottom with a "Send" button for submitting queries.

**FR-55:** The document upload interface must include:
   - A file picker supporting multiple file selection
   - A dropdown menu populated from the `/collections` endpoint showing available knowledge bases and "Auto-Map" option
   - "Auto-Map" selected as the default option
   - Upload progress indicator showing percentage and file-by-file status
   - Success/error notifications for each upload

**FR-56:** The interface must be responsive and usable on desktop browsers (Chrome, Firefox, Safari, Edge).

**FR-57:** The interface must display source citations in an expandable/collapsible format below each AI response.

**FR-58:** At the end of each conversation completion, the system must display a satisfaction feedback interface with:
   - A "Thumbs Up" button (👍) for positive feedback
   - A "Thumbs Down" button (👎) for negative feedback
   - An optional text input box for additional feedback comments
   - A "Submit Feedback" button to submit the rating and optional comments

**FR-59:** The satisfaction feedback interface must appear immediately after the final AI response in a conversation, positioned prominently but non-intrusively below the last message.

**FR-60:** Representatives must be able to submit satisfaction feedback (thumbs up or thumbs down) without being required to provide optional text comments.

**FR-61:** The system must store satisfaction feedback with each conversation session, including:
   - Rating (thumbs up or thumbs down)
   - Optional feedback text (if provided)
   - Session ID
   - Timestamp
   - Agent that handled the conversation

---

## 5. Non-Goals (Out of Scope)

**NG-1:** **Direct External Customer Access:** The system will not provide a customer-facing interface. This MVP is exclusively for internal customer service representatives.

**NG-2:** **Voice/Phone Integration:** The system will not support voice input or phone-based interactions. All interactions are text-based through the web interface.

**NG-3:** **Production-Grade Authentication/Authorization:** The MVP will not include enterprise SSO, role-based access control, or production-grade user management. Basic session-based authentication is sufficient for proof-of-concept.

**NG-4:** **Multi-Language Support:** The MVP will support English language only. Internationalization and translation features are out of scope.

**NG-5:** **Integration with Existing Ticketing Systems:** The system will not integrate with ServiceNow, Zendesk, JIRA, or other ticketing/CRM platforms. Integration points may be added in future phases.

**NG-6:** **Real-Time Inventory Lookups:** The system will not perform real-time queries to inventory management systems, ERP systems, or supply chain databases. It relies solely on documents ingested into the knowledge bases.

**NG-7:** **Order Processing or Payment Handling:** The system will not process orders, payments, or transactions. It provides information only.

**NG-8:** **Mobile Application:** The MVP will be web-based only. Native mobile apps (iOS/Android) are out of scope.

**NG-9:** **Advanced Analytics Dashboard:** While basic usage metrics are captured, a comprehensive analytics dashboard with advanced visualizations is out of scope for MVP.

**NG-10:** **File Attachments in Chat:** The system will not support uploading file attachments within chat messages. Document uploads are handled exclusively through the dedicated document upload interface.

**NG-11:** **Industry Certifications:** No AS9100, ISO 9001, or other aerospace industry certification compliance requirements in this MVP phase. The system focuses on functional proof-of-concept rather than regulatory certification.

**NG-12:** **Multi-Agent Conversation Handoffs:** The MVP does not support complex multi-agent coordination where one agent passes context to another mid-conversation. The supervisor routes queries to a single agent per turn.

---

## 6. Design Considerations

### 6.1 User Interface Design

- **UI Framework:** Next.js with React and shadcn/ui component library for modern, accessible UI components
- **Styling:** TailwindCSS for responsive design and consistent styling
- **Color Scheme:** Professional, aerospace-themed color palette (blues, grays) suitable for enterprise use
- **Typography:** Clear, readable fonts optimized for extended reading sessions

### 6.2 Chat Interface Components

- **Message List:** Scrollable container with alternating background colors for representative vs. AI messages
- **Streaming Indicator:** Visual indicator (e.g., typing dots) when AI is generating a response
- **Agent Badge:** Small badge/icon indicating which agent generated each response (Billing/Technical/Policy)
- **Citation Toggle:** Expandable section below each AI response showing source citations with document names and excerpts
- **Input Field:** Multi-line text area with character count and send button
- **Satisfaction Feedback UI:** Feedback interface displayed at the end of each conversation with:
  - Large, accessible thumbs up (👍) and thumbs down (👎) buttons
  - Optional text area for feedback comments (placeholder: "Optional: Add your feedback...")
  - Submit button to send feedback
  - Confirmation message after submission (e.g., "Thank you for your feedback!")

### 6.3 Document Upload Interface

- **File Drop Zone:** Drag-and-drop area with file picker button
- **Knowledge Base Selector:** Dropdown menu with "Auto-Map" as first option (selected by default), followed by billing_knowledge_base, technical_knowledge_base, policy_knowledge_base
- **File Preview:** List of selected files with names, sizes, and remove buttons
- **Progress Indicator:** Progress bar showing overall upload progress and per-file status
- **Success/Error Feedback:** Toast notifications or inline messages for upload results

### 6.4 Responsive Design

- **Desktop-First:** Optimized for desktop/laptop use (representatives typically use desktop computers)
- **Minimum Viewport:** Support for screens as small as 1024x768 pixels
- **Touch-Friendly:** Ensure buttons and interactive elements are adequately sized for touch interaction on tablets (if used)

### 6.5 Accessibility

- **Keyboard Navigation:** Full keyboard support for all interactive elements
- **Screen Reader Support:** Proper ARIA labels and semantic HTML
- **Color Contrast:** WCAG AA compliance for text and background colors

---

## 7. Technical Considerations

### 7.1 Technology Stack

**TC-1:** **Backend Framework:** Python 3.11+ with FastAPI for high-performance async API development

**TC-2:** **Frontend Framework:** Next.js 14.x with React 18.x for server-side rendering and client-side interactivity

**TC-3:** **AI Framework:** LangChain v1.0+, LangGraph (for custom orchestration workflows if needed)

**TC-4:** **Agent Architecture:** Use `create_agent()` from `langchain.agents` for all agents (supervisor and workers) following the v1.0 supervisor pattern with tool calling

**TC-5:** **LLM Providers:** 
   - OpenAI API (GPT-4o-mini for worker agents)
   - AWS Bedrock (Claude 3 Haiku or Nova Lite for supervisor routing)

**TC-6:** **Vector Database:** ChromaDB 0.4+ with local persistence (SQLite backend)

**TC-7:** **Document Processing:** PyPDFLoader, TextLoader, UnstructuredMarkdownLoader, RecursiveCharacterTextSplitter from LangChain

**TC-8:** **Memory/State:** InMemorySaver() from `langgraph.checkpoint.memory` for conversation persistence

**TC-9:** **Embeddings:** OpenAI embeddings API (text-embedding-3-small, 1536 dimensions)

### 7.2 Agent Architecture Implementation

**TC-10:** **Supervisor Agent Creation:**
   - Use `create_agent()` from `langchain.agents`
   - Provide descriptive `name` parameter (e.g., "supervisor_agent")
   - Configure system prompt emphasizing query routing to appropriate worker tools
   - Include tools list with wrapped worker agents
   - Use AWS Bedrock model: "bedrock:claude-3-haiku" or similar
   - Include checkpointer: `InMemorySaver()`

**TC-11:** **Worker Agent Creation:**
   - Create each worker agent (Billing, Technical, Policy) using `create_agent()`
   - Provide descriptive `name` parameter (e.g., "billing_support_agent", "technical_support_agent", "policy_compliance_agent")
   - Configure system prompts emphasizing:
     - Domain expertise
     - **CRITICAL:** Include ALL results, findings, and details in final response (supervisor only sees final message)
     - Source citation requirements
   - Include appropriate RAG retrieval tools for each agent's knowledge base
   - Use OpenAI model: "openai:gpt-4o-mini"
   - Include checkpointer: `InMemorySaver()`

**TC-12:** **Tool Wrapping:**
   - Wrap each worker agent as a tool using `@tool` decorator
   - Tool descriptions must clearly indicate when supervisor should call each tool:
     - Billing tool: "Handle billing inquiries, pricing questions, contract terms, invoices"
     - Technical tool: "Handle technical questions, component specifications, bug reports, technical manuals"
     - Policy tool: "Handle regulatory compliance questions, FAA/EASA regulations, policy inquiries"
   - Tool functions invoke worker agents and return final response content

**TC-13:** **RAG Retrieval Tools:**
   - Create `@tool` decorated functions for each knowledge base:
     - `search_billing_kb(query: str) -> str`
     - `search_technical_kb(query: str) -> str`
     - `search_policy_kb(query: str) -> str`
   - Each tool queries ChromaDB collection, retrieves top k documents, and returns formatted context

**TC-14:** **Emergency Escalation Tool:**
   - Create `@tool` decorated function `detect_emergency(query: str) -> str`
   - Analyzes query for safety-critical keywords and intent
   - Returns escalation message with contact information if emergency detected

### 7.3 Conversation Flow

**TC-15:** **Supervisor Pattern Flow:**
   1. Representative submits query through web interface → FastAPI receives POST /chat
   2. FastAPI invokes supervisor agent with `thread_id` from session
   3. Supervisor agent analyzes query using AWS Bedrock (fast, cost-effective)
   4. Supervisor calls appropriate worker tool based on query intent
   5. Worker agent executes:
      - Receives query from supervisor
      - Calls its RAG tool to retrieve relevant documents
      - Generates response with citations using OpenAI (high quality)
      - Returns complete response to supervisor
   6. Supervisor formats response and streams tokens to frontend via SSE
   7. Conversation saved with `thread_id` using InMemorySaver()

**TC-16:** **Code Pattern Example:**
```python
# Supervisor agent invokes worker tool
config = {"configurable": {"thread_id": session_id}}
result = supervisor_agent.invoke({"messages": [user_message]}, config)

# Worker agent invoked by supervisor tool
# Worker receives message, calls RAG tool, generates response
worker_response = billing_agent.invoke({"messages": [query]}, config)
return worker_response["messages"][-1].content  # Return final message content
```

### 7.4 Context Engineering

**TC-17:** **Model Context (Transient Changes):**
   - Use `@dynamic_prompt` decorator for adaptive system prompts based on conversation length or query complexity
   - Inject relevant context (e.g., conversation history, document categories) into agent prompts dynamically
   - Consider conversation-specific instructions that adapt based on query patterns

**TC-18:** **Tool Context (Persistent Changes):**
   - Tools use `ToolRuntime` to access state (conversation history), store (long-term preferences), and config (user ID, permissions)
   - Use `Command` from `langgraph.types` to persistently update state from tools
   - Pass conversation context via tool parameters when invoking worker agents

**TC-19:** **Life-cycle Context:**
   - Use `@before_model` hooks for safety checks (emergency detection, content moderation)
   - Use `@after_model` hooks for logging, formatting, and metrics collection
   - Consider `SummarizationMiddleware` if conversations exceed token limits (implement if needed for MVP)

### 7.5 Error Handling

**TC-20:** The system must handle and gracefully recover from:
   - LLM API failures (rate limits, timeouts, service outages)
   - ChromaDB connection errors or query failures
   - Document ingestion errors (corrupted files, unsupported formats)
   - Network errors during streaming responses

**TC-21:** Error messages must be user-friendly and actionable, indicating what went wrong and suggesting next steps (e.g., "Unable to connect to knowledge base. Please try again or contact support.")

**TC-22:** The system must log all errors with sufficient context (timestamp, session ID, query content, error type) for debugging and monitoring.

### 7.6 Performance Requirements

**TC-23:** **Response Time Target:** The system must provide initial responses within **<30 seconds** from query submission, including:
   - Supervisor routing decision
   - Worker agent retrieval
   - Response generation
   - First token streamed to frontend

**TC-24:** **Streaming Performance:** Tokens should stream to the frontend within 100ms of generation to provide smooth real-time experience.

**TC-25:** **Document Ingestion:** The system must process and store uploaded documents within reasonable timeframes:
   - Small files (<50 KB): <10 seconds
   - Medium files (50-100 KB): <30 seconds
   - Large files (100-200 KB): <60 seconds

**TC-26:** **Concurrent Sessions:** The system must support at least 10 concurrent representative sessions without degradation in response time.

### 7.7 Data Persistence

**TC-27:** **Conversation History:** Conversation history must persist in memory for active sessions using `InMemorySaver()` from `langgraph.checkpoint.memory`. Only the last 3 conversations per representative are retained (FIFO policy).

**TC-28:** **Vector Database:** ChromaDB must use local persistence (SQLite backend) with data stored in `./chroma_db` directory. Collections are created on first document ingestion.

**TC-29:** **Session Management:** Session IDs (thread_ids) are generated as UUIDs and stored in browser localStorage for persistence across page refreshes.

### 7.8 Configuration

**TC-30:** **Environment Variables Required:**
   - `OPENAI_API_KEY`: API key for OpenAI (embeddings and worker agents)
   - `AWS_ACCESS_KEY_ID`: AWS access key for Bedrock
   - `AWS_SECRET_ACCESS_KEY`: AWS secret key for Bedrock
   - `AWS_REGION`: AWS region for Bedrock (e.g., "us-east-1")
   - `ESCALATION_EMAIL`: Emergency escalation contact (default: "ski@aerospace-co.com")

**TC-31:** **Environment Variables Optional:**
   - `LANGSMITH_TRACING`: Enable LangSmith tracing (set to "true" for development)
   - `LANGSMITH_API_KEY`: LangSmith API key for tracing
   - `LANGSMITH_PROJECT`: LangSmith project name for tracing

**TC-32:** **Configuration Files:**
   - `requirements.txt`: Python dependencies (FastAPI, LangChain, ChromaDB, etc.)
   - `package.json`: Frontend dependencies (Next.js, React, shadcn/ui, etc.)
   - `.env`: Environment variables (not committed to repository)

### 7.9 Development Methodology

**TC-33:** The project must be developed following the **Vibe Coding Strategy**:
   - Natural language-driven, iterative approach
   - Developer acts as "conductor," guiding and validating AI-generated output
   - Conversational loop with AI tools generating code
   - **NOTE:** NO MAX MODE - use standard AI assistance patterns

---

## 8. Success Metrics

**SM-1:** **Primary Metric - Representative Satisfaction:** Achieve and maintain at least **80% thumbs up rating** from representatives, measured through thumbs up/thumbs down voting buttons displayed at the end of each conversation completion.

**SM-2:** **Feedback Submission Rate:** At least 70% of completed conversations receive satisfaction feedback (thumbs up or thumbs down) from representatives.

**SM-3:** **Response Time:** Achieve average response time of **<30 seconds** from query submission to first token streamed.

**SM-4:** **Adoption Rate:** At least 70% of customer service representatives use the system at least once per week within 30 days of launch.

**SM-5:** **Accuracy:** At least 90% of AI responses include relevant source citations that representatives can verify.

**SM-6:** **Agent Routing Accuracy:** At least 85% of queries are correctly routed to the appropriate specialized agent by the supervisor.

**SM-7:** **Emergency Detection:** 100% of safety-critical queries trigger the emergency escalation mechanism.

**SM-8:** **Document Ingestion Success Rate:** At least 95% of uploaded documents are successfully processed and stored in the correct knowledge base collection.

**SM-9:** **System Uptime:** Achieve 99% uptime during business hours (excluding planned maintenance).

**SM-10:** **Error Rate:** Keep unhandled errors (500-level responses) below 1% of all API requests.

**SM-11:** **Conversation Retention:** System successfully retains and retrieves conversation history for 95% of sessions within the 3-conversation FIFO limit.

---

## 9. Open Questions

**OQ-1:** ✅ **Customer Satisfaction Scoring Method** - **ANSWERED:** Simple thumbs up/thumbs down voting buttons with optional feedback message box, displayed at the end of each conversation completion.

**OQ-2:** ✅ **Conversation Logging & Retention Policy** - **ANSWERED:** System logs only the last 3 chat conversations per representative following FIFO (First In, First Out) retention policy.

**OQ-3:** ✅ **Knowledge Base Update Process** - **ANSWERED:** Document upload interface allows authorized representatives to upload documents. Auto-Map automatically categorizes documents, or representatives can manually select target knowledge base.

**OQ-4:** ✅ **User Permissions/UI Differences** - **ANSWERED:** Scope limited to internal customer service representatives only. No external customer-facing features.

**OQ-5:** ✅ **Escalation Process for Safety-Critical Queries** - **ANSWERED:** Emergency escalation contact: **ski@aerospace-co.com**. System detects safety-critical queries and displays escalation notice immediately.

**OQ-6:** ✅ **Industry Standards/Certifications** - **ANSWERED:** No industry certifications (AS9100, ISO 9001, etc.) required for MVP phase.

**OQ-7:** ✅ **File Attachments in Chat** - **ANSWERED:** System does not support file attachments in chat messages. Document uploads handled through dedicated upload interface.

**OQ-8:** ✅ **Expected Document Volume** - **ANSWERED:** System designed for approximately 100 files per knowledge base collection, average file size 100 KB, totaling ~10 MB per collection.

**OQ-9:** ✅ **Mock Aerospace Data** - **ANSWERED:** Use public FAA documents and synthetic data as appropriate for demonstration and testing purposes.

**OQ-10:** **Company Branding:** What is the official company name and logo? - **ANSWERED:** Using placeholder "The Aerospace Company" with generic airplane logo for MVP.

**OQ-11:** **Response Time Targets:** What is the target response time? - **ANSWERED:** <30 seconds from query submission to first token streamed.

**OQ-12:** **Knowledge Base Content Mapping:** What specific document types belong in each knowledge base? - **ANSWERED:** 
   - Billing KB: parts catalogs with pricing, contracts, invoices
   - Technical KB: bug reports, technical manuals, specifications, technical publications
   - Policy KB: FAA/EASA regulations, Govt/DFARs policies, data governance, customer support policies, invoicing policies (US Govt defense and commercial)

---

## 10. Development Methodology

This project will be developed using the **Vibe Coding Strategy**:

- **Description:** A natural language-driven, iterative approach where the developer describes the desired software behavior in plain language prompts, and AI tools generate the code. The developer's role is to act as a "conductor," guiding, shaping, and validating the AI-generated output in a conversational loop.
- **Key Principle:** NO MAX MODE - use standard AI assistance patterns throughout development.
- **Reference:** https://github.com/snarktank/ai-dev-tasks/tree/main

---

## 11. Acceptance Criteria

The MVP will be considered complete when all of the following criteria are met:

**AC-1:** Representatives can open the web interface titled "The Aerospace Company Customer Service Agent" with airplane logo prominently displayed.

**AC-2:** Representatives can submit text-based queries through the chat interface and receive streaming AI responses in real-time.

**AC-3:** The supervisor agent correctly routes at least 85% of queries to the appropriate specialized agent (Billing, Technical, or Policy).

**AC-4:** Each AI response displays the name of the agent that generated it (Billing Support, Technical Support, or Policy & Compliance).

**AC-5:** Each AI response includes source citations with document names and relevant excerpts.

**AC-6:** Representatives can upload documents through the upload interface, which displays a dropdown menu listing available knowledge base collections (billing_knowledge_base, technical_knowledge_base, policy_knowledge_base) plus "Auto-Map" option.

**AC-7:** The "Auto-Map" option is selected by default in the knowledge base dropdown.

**AC-8:** When "Auto-Map" is selected, uploaded documents are automatically categorized into the appropriate knowledge base collection based on content analysis.

**AC-9:** When a specific knowledge base is manually selected, all uploaded documents are stored in that selected collection.

**AC-10:** The system successfully processes and stores uploaded documents (PDF, TXT, Markdown, JSON) in ChromaDB with embeddings.

**AC-11:** Representatives can view conversation history for their current session.

**AC-12:** When a safety-critical query is detected, the system displays an escalation notice with contact information: **john.doe@aerospace-co.com**.

**AC-13:** Conversation history persists for the last 3 conversations per representative following FIFO (first in first out) retention policy.

**AC-14:** Representatives can switch between existing sessions (up to 3 historical conversations visible).

**AC-15:** The system achieves average response time of <30 seconds from query submission to first token streamed.

**AC-16:** The system uses LangChain v1.0 `create_agent()` function for all agents, following supervisor pattern with tool calling.

**AC-17:** All three specialized agents (Billing, Technical, Policy) implement their designated retrieval strategies (Hybrid RAG/CAG, Pure RAG, Pure CAG).

**AC-18:** At the end of each conversation completion, representatives see satisfaction feedback interface with thumbs up and thumbs down buttons, optional feedback text box, and submit functionality.

**AC-19:** Representatives can submit satisfaction feedback (thumbs up or thumbs down) with or without optional text comments.

**AC-20:** The system successfully stores satisfaction feedback with session ID, timestamp, rating, optional comment, and agent information.

**AC-21:** The demonstration video shows:
   - System overview and architecture
   - Chat interface with queries routed to each agent type
   - Document upload with both Auto-Map and manual selection
   - Emergency escalation detection
   - Source citations in responses
   - Satisfaction feedback interface (thumbs up/down with optional comments)

---

## 12. Submission Deliverables

### 12.1 GitHub Repository

A public GitHub repository containing:
- Complete source code for backend (Python/FastAPI)
- Complete source code for frontend (Next.js/React)
- Comprehensive README.md with:
  - Project overview and architecture
  - Environment setup instructions
  - Dependency installation steps
  - Local development and running instructions
  - API endpoint documentation
  - Knowledge base setup and ingestion guide
- Code comments and documentation following best practices

### 12.2 Unlisted YouTube Video

A 5-10 minute unlisted YouTube video demonstrating:
1. **System Overview (1-2 minutes):**
   - Architecture explanation (supervisor pattern, multi-agent system)
   - Technology stack overview
   - Key features summary

2. **Live Application Demo (3-5 minutes):**
   - Chat interface walkthrough
   - Example query routed to Billing Support Agent with response and citations
   - Example query routed to Technical Support Agent with response and citations
   - Example query routed to Policy & Compliance Agent with response and citations
   - Emergency escalation detection demonstration
   - Document upload interface showing Auto-Map and manual selection

3. **Code Walkthrough (2-3 minutes):**
   - Supervisor agent implementation using `create_agent()`
   - Worker agent creation and tool wrapping
   - RAG retrieval tool implementations
   - LangGraph conversation flow
   - FastAPI streaming endpoint
   - Frontend-backend integration

### 12.3 Documentation

- API documentation (OpenAPI/Swagger specification)
- Architecture diagrams (agent flow, data flow)
- Development methodology notes (Vibe Coding Strategy application)

---

## 13. Appendix A: Example Queries by Agent Type

### Billing Support Agent (Hybrid RAG/CAG)

Representatives might enter these queries when helping customers with billing inquiries:

- "What is the pricing for part number ABC-123?"
- "What are the payment terms for contract #2024-001?"
- "How do I process a refund for invoice INV-456?"
- "What is the pricing policy for bulk orders of components?"
- "Can you explain the invoicing process for US Government defense contracts vs. commercial customers?"

### Technical Support Agent (Pure RAG)

Representatives might enter these queries when helping customers with technical questions:

- "What are the specifications for the landing gear assembly in Model X-200?"
- "I need information about bug report #1234 regarding hydraulic system failure."
- "What is the recommended maintenance procedure for engine component Y?"
- "Can you provide details about the technical service bulletin TS-2024-15?"
- "What are the system requirements for integrating component Z into aircraft Model Y?"

### Policy & Compliance Agent (Pure CAG)

Representatives might enter these queries when helping customers with regulatory or policy questions:

- "What are the FAA requirements for component certification?"
- "What is our company's data governance policy for customer information?"
- "What are the service level agreements for incident reporting?"
- "What is the policy for handling ageing invoices over 90 days?"
- "What are the DFARs compliance requirements for our defense contracts?"
- "What are the invoicing policies for commercial vs. government customers?"

### Emergency Escalation Examples

These queries should trigger immediate escalation to **ski@aerospace-co.com**:

- "URGENT: Aircraft in flight experiencing hydraulic failure"
- "EMERGENCY: Customer reporting safety incident with component failure"
- "Critical: Need immediate assistance with in-flight emergency"
- "Safety Alert: Potential defect in recently shipped components"

---

**Document End**

