# Conversation Summary & Actions for PRD Development

## Document Overview
This document captures the complete conversation flow, user responses, and all corresponding actions taken to develop the Product Requirements Document (PRD) for the Aerospace Customer Service AI System.

---

## Conversation 1: Initial PRD Creation

### User Request
> "Use @create-prd.md. The primary goal of this project is to develop a customer service application powered by a multi-agent AI system for an Aerospace company. Reference these files to help you: @agentic-customer-specs.md @ARCHITECTURE.md"

### Clarifying Questions Asked

#### Question 1: Primary Problem/Goal
**Options Provided:**
- A) Reduce response time for customer inquiries across multiple departments
- B) Improve accuracy and consistency of technical support responses
- C) Scale customer service without proportionally increasing headcount
- D) All of the above
- E) Other (please specify)

**User Response:** `1-D` (All of the above)

---

#### Question 2: Target Users
**Options Provided:**
- A) Aerospace customers (airlines, defense contractors, space agencies)
- B) Internal customer service representatives (human-in-the-loop)
- C) Both external customers and internal representatives
- D) Other (please specify)

**User Response:** `2-C` (Both external customers and internal representatives)

---

#### Question 3: Aerospace-Specific Agent Specializations
**Options Provided:**
- A) Safety & Compliance Agent (FAA regulations, safety bulletins)
- B) Parts & Maintenance Agent (component specs, maintenance schedules)
- C) Flight Operations Agent (operational procedures, flight planning)
- D) Contract & Procurement Agent (RFPs, contract terms)
- E) Some combination of the above (please specify which)
- F) Stick with the standard three agents for MVP

**User Response:** `3-F` (Stick with the standard three agents for MVP)

---

#### Question 4: Data Sources
**Options Provided:**
- A) Technical manuals and service bulletins
- B) Regulatory compliance documents (FAA/EASA)
- C) Parts catalogs and maintenance schedules
- D) Contract documents and pricing guides
- E) All of the above
- F) Other (please specify)

**User Response:** `4-E` (All of the above)

---

#### Question 5: Success Criteria
**Options Provided:**
- A) Response accuracy (X% correct answers)
- B) Response time (under X seconds)
- C) Customer satisfaction scores
- D) Reduction in human agent escalations
- E) Multiple metrics (please specify which)

**User Response:** `5-C` (Customer satisfaction scores)

---

#### Question 6: Scope Boundaries
**Options Provided:**
- A) Integration with existing ticketing systems (ServiceNow, Zendesk)
- B) Multi-language support
- C) Voice/phone integration
- D) Production-grade authentication/authorization
- E) Other specific exclusions (please specify)

**User Response:** `6-C,D` (Voice/phone integration AND Production-grade authentication/authorization)

---

#### Question 7: Critical Edge Cases
**Options Provided:**
- A) Handling ITAR/EAR restricted information
- B) Emergency/critical safety queries requiring immediate human escalation
- C) Complex multi-part queries spanning multiple domains
- D) Version control for technical documents (ensuring latest revisions)
- E) All of the above
- F) Other (please specify)

**User Response:** `7-B` (Emergency/critical safety queries requiring immediate human escalation)

---

### Actions Taken: Initial PRD Creation
**File Created:** `/tasks/0001-prd-aerospace-customer-service.md`

**PRD Structure Implemented:**
1. ✅ Introduction with problem statement and solution
2. ✅ Goals (6 specific objectives)
3. ✅ User Stories (11 total covering external customers, internal reps, and critical safety scenarios)
4. ✅ Functional Requirements (42 detailed requirements across 10 subsections):
   - Core Chat Functionality (FR-1 to FR-5)
   - Multi-Agent Orchestration (FR-6 to FR-10)
   - Retrieval Strategies (FR-11 to FR-14)
   - Document Ingestion (FR-15 to FR-21)
   - Emergency Escalation (FR-22 to FR-25)
   - Session Management (FR-26 to FR-29)
   - LLM Provider Strategy (FR-30 to FR-32)
   - Vector Database (FR-33 to FR-36)
   - API Endpoints (FR-37 to FR-40)
   - User Interface (FR-41 to FR-45)
5. ✅ Non-Goals (8 specific exclusions)
6. ✅ Design Considerations (UI/UX, components, responsive design)
7. ✅ Technical Considerations (tech stack, state management, LangGraph workflow, error handling, performance, persistence, configuration)
8. ✅ Success Metrics (primary: customer satisfaction; 10 supporting metrics)
9. ✅ Open Questions (10 questions for further clarification)
10. ✅ Development Methodology (Vibe Coding Strategy)
11. ✅ Acceptance Criteria (14 criteria for MVP completion)
12. ✅ Submission Deliverables (GitHub repo, YouTube video, documentation)
13. ✅ Appendix A: Example queries by agent type

**Key Features Included:**
- Multi-agent system with three specialized agents (Billing, Technical Support, Policy & Compliance)
- Hybrid RAG/CAG, Pure RAG, and Pure CAG retrieval strategies
- Emergency escalation system for safety-critical queries
- Document upload and ingestion pipeline
- Customer satisfaction scoring as primary metric
- Support for both external and internal users

---

## Conversation 2: PRD Regeneration with Modifications

### User Request
> "Please regenerate the PRD with following modifications..."

### Modification 1: User Focus
**Request:** Remove all target external aerospace customer and use cases. Just focus on internal customer service representatives.

**Actions Taken:**
1. ✅ **Updated Introduction (Section 1):**
   - Changed problem statement to focus on challenges faced by internal representatives
   - Updated solution description to emphasize representative empowerment
   - Reframed system as tool for representatives (not direct customer access)

2. ✅ **Updated Goals (Section 2):**
   - Changed Goal 1: "Enable representatives to deliver faster, more accurate responses"
   - Changed Goal 2: "Reduce research time" instead of "response time"
   - Added Goal 5: "Empower Representatives"

3. ✅ **Completely Rewrote User Stories (Section 3):**
   - **Removed:** All external customer user stories (US-1 through US-4)
   - **Added Internal Representative Stories (US-1 to US-8):**
     - US-1: Input technical questions, receive source-backed answers
     - US-2: Automatic routing to appropriate agent
     - US-3: Quick access to billing information
     - US-4: See source citations for verification
     - US-5: Maintain conversation history
     - US-6: Upload new documents to keep system current
     - US-7: Manually select knowledge base for uploads
     - US-8: Real-time streaming responses
   - **Added Team Lead Stories (US-9 to US-10):**
     - US-9: Review conversation histories for training
     - US-10: See usage metrics for adoption/ROI
   - **Updated Critical Safety Story (US-11):**
     - Reframed for representatives handling emergency calls

4. ✅ **Updated Non-Goals (Section 5):**
   - Added NG-1: "Direct External Customer Access" - explicitly excluded customer-facing interface
   - Updated all language to reflect internal-user-only scope

5. ✅ **Updated Example Queries (Appendix A):**
   - Prefaced all examples with "Representatives might enter these queries when helping customers..."
   - Added context that representatives are intermediaries

---

### Modification 2: Enhanced Document Upload (FR-15/FR-16)
**Request:** Add ability for user to specify single target knowledge base from dropdown list of collections. System should also allow auto-map capability by default.

**Actions Taken:**
1. ✅ **Updated FR-16 (formerly FR-15):**
   - Added **Manual Knowledge Base Selection**: Dropdown menu listing available collections
   - Added **Auto-Map Default Option**: Selected by default, automatically categorizes documents
   - Added **Real-time Collection Detection**: Dropdown populated by querying ChromaDB backend

2. ✅ **Restructured Requirements:**
   - FR-17: Document format support (PDF, TXT, Markdown, JSON)
   - FR-18: Auto-Map mode behavior (automatic categorization)
   - FR-19: Manual selection mode behavior (all docs go to selected collection)
   - FR-20: Processing pipeline
   - FR-21: Upload progress display
   - FR-22: File validation

3. ✅ **Added API Endpoint (FR-38/FR-39):**
   - `GET /collections`: List all available knowledge base collections from ChromaDB

4. ✅ **Updated UI Requirements (FR-44/FR-45):**
   - Document upload interface must include dropdown populated from `/collections` endpoint
   - "Auto-Map" option as default selection in dropdown

5. ✅ **Updated Acceptance Criteria:**
   - AC-6: Dropdown displays available knowledge base collections
   - AC-7: "Auto-Map" option selected by default
   - AC-8: Auto-Map automatically categorizes documents
   - AC-9: Manual selection stores all docs in selected collection
   - AC-18: Demo video must show both Auto-Map and manual selection

---

### Modification 3: Professional Branding
**Request:** Frontend UI must be titled professionally as "The Aerospace Company Customer Service Agent" with an airplane logo.

**Actions Taken:**
1. ✅ **Added FR-42 (formerly FR-41):**
   - Application titled: **"The Aerospace Company Customer Service Agent"**
   - Prominently displayed in header
   - Includes airplane logo icon

2. ✅ **Updated Acceptance Criteria:**
   - AC-1: Representative can open interface titled "The Aerospace Company Customer Service Agent" with airplane logo

---

### Modification 4: Open Questions Answered

#### OQ-1: Customer Satisfaction Scoring Method
**User Response:** In-app survey

**Actions Taken:**
- ✅ Marked question as answered
- ✅ Updated Success Metrics (SM-1 to SM-3) to specify in-app survey after conversation ends or 5+ message exchanges

---

#### OQ-2: Conversation Logging & Retention Policy
**User Response:** System must log only the last 3 chat conversations. All chat conversation logs will follow FIFO for a retention policy.

**Actions Taken:**
- ✅ Marked question as answered
- ✅ **Updated FR-28 (formerly FR-27):** "storing only the last 3 chat conversations per representative following a FIFO (First In, First Out) retention policy"
- ✅ **Updated TC-23 (formerly TC-17):** Added FIFO retention detail
- ✅ **Updated Acceptance Criteria:**
  - AC-13: Conversation history persists only last 3 conversations per representative (FIFO)
  - AC-14: Representatives can switch between existing sessions (up to 3 historical)

---

#### OQ-3: Knowledge Base Update Process
**User Response:** Admin upload

**Actions Taken:**
- ✅ Marked question as answered
- ✅ Clarified that document upload interface is the admin upload mechanism

---

#### OQ-4: User Permissions/UI Differences
**User Response:** Limit scope to only internal users. Do not develop anything for external users.

**Actions Taken:**
- ✅ Marked question as answered
- ✅ Added NG-1 in Non-Goals: "Direct External Customer Access"
- ✅ Removed all external customer user stories and use cases throughout document

---

#### OQ-5: Escalation Process for Safety-Critical Queries
**User Response:** Use following email address for escalation: ski@aerospace-co.com

**Actions Taken:**
- ✅ Marked question as answered
- ✅ **Updated FR-24 (formerly FR-23):** "Provide emergency contact information: **ski@aerospace-co.com**"
- ✅ **Updated TC-28 (formerly TC-22):** Added `ESCALATION_EMAIL` environment variable (default: ski@aerospace-co.com)
- ✅ **Updated Acceptance Criteria:**
  - AC-12: System displays escalation notice with email contact **ski@aerospace-co.com**
- ✅ **Updated Appendix A:** Safety-critical examples show escalation to **ski@aerospace-co.com**

---

#### OQ-6: Industry Standards/Certifications
**User Response:** No

**Actions Taken:**
- ✅ Marked question as answered
- ✅ Added NG-11 in Non-Goals: "Industry Certifications: No AS9100, ISO 9001, or other aerospace industry certification compliance in this MVP phase"

---

#### OQ-7: File Attachments in Chat
**User Response:** No system should not support upload of file attachments in chat messages

**Actions Taken:**
- ✅ Marked question as answered
- ✅ Added NG-10 in Non-Goals: "File Attachments in Chat: The system will not support uploading file attachments within chat messages. Document uploads are handled exclusively through the dedicated document upload interface."

---

#### OQ-8: Expected Document Volume
**User Response:** Expect no more than 100 files per collection each file no more than 100 KB in size on average.

**Actions Taken:**
- ✅ Marked question as answered
- ✅ **Updated TC-25 (formerly TC-19):** "The system is designed to handle approximately 100 files per knowledge base collection, with average file size of 100 KB, totaling approximately 10 MB per collection."

---

#### OQ-9: Mock Aerospace Data
**User Response:** Use public FAA documents and synthetic data as appropriate

**Actions Taken:**
- ✅ Marked question as answered
- ✅ Noted in Open Questions section that public FAA documents and synthetic data should be used for demonstration and testing

---

### Summary of Modifications - Round 2

**Total Changes Made:**
- ✅ Removed 4 external customer user stories
- ✅ Added 11 internal representative-focused user stories
- ✅ Added 1 new Non-Goal (NG-1: Direct External Customer Access)
- ✅ Added 1 new Non-Goal (NG-10: File Attachments in Chat)
- ✅ Added 1 new Non-Goal (NG-11: Industry Certifications)
- ✅ Enhanced document upload requirements (FR-16 to FR-22)
- ✅ Added professional branding requirement (FR-42)
- ✅ Added new API endpoint (GET /collections)
- ✅ Updated 9 Open Questions with answers
- ✅ Added email escalation address throughout document
- ✅ Specified FIFO retention policy for conversations
- ✅ Updated technical considerations for expected data volumes
- ✅ Enhanced acceptance criteria with specific features

---

## Conversation 3: LangChain v1.0 Alignment

### User Request
> "@langchain-langgraph-v1.mdc Regenerate the PRD in context of the newly added rule"

### Context
User provided comprehensive LangChain & LangGraph v1.0 Development Guidelines emphasizing:
- Deprecation of LCEL (LangChain Expression Language)
- Use of `create_agent()` from `langchain.agents` as standard approach
- Supervisor pattern with tool calling for multi-agent systems
- Context engineering patterns (Model, Tool, Life-cycle Context)
- Simplicity first: avoid manual LangGraph StateGraph unless truly necessary

---

### Actions Taken: LangChain v1.0 Compliance Updates

#### 1. Updated Solution Statement (Introduction)
**Before:** "A multi-agent AI system powered by LangGraph..."

**After:** "A multi-agent AI system built with LangChain v1.0 that assists internal customer service representatives by intelligently routing customer inquiries to specialized AI agents. The system uses a **supervisor pattern** where an orchestrator agent coordinates specialized worker agents (Billing, Technical Support, Policy & Compliance) as tools."

**Rationale:** Explicitly mentioned v1.0 and supervisor pattern to set correct expectations

---

#### 2. Completely Rewrote Multi-Agent Orchestration (Section 4.2)

**Before (Generic Orchestration):**
- FR-6: "supervisor/orchestrator agent"
- FR-7: Three specialized worker agents
- FR-8: "classify each query and route to exactly one agent"
- FR-9: Visual indication of agent
- FR-10: Support agent handoffs

**After (LangChain v1.0 Supervisor Pattern):**
- ✅ **FR-6:** Implement **supervisor agent** using LangChain v1.0 tool calling pattern
- ✅ **FR-7:** Create three specialized worker agents using `create_agent()` from `langchain.agents`
- ✅ **FR-8:** Each specialized worker agent wrapped as tool using `@tool` decorator
- ✅ **FR-9:** Supervisor uses tool descriptions to determine which agent to invoke
- ✅ **FR-10:** Visual indication by parsing tool execution results
- ✅ **FR-11:** Worker agents must include all information in final responses (supervisor only sees final message)

**Rationale:** Aligned with v1.0 best practice of supervisor pattern where workers are tools, not separate graph nodes

---

#### 3. Updated Retrieval Strategies Numbering (Section 4.3)
**Actions:** Renumbered FR-11 to FR-15 → FR-12 to FR-15 to avoid conflicts after adding FR-11

---

#### 4. Updated Document Ingestion (Section 4.4)
**Actions:**
- ✅ Changed FR-15 → FR-16
- ✅ Specified "RecursiveCharacterTextSplitter" (proper v1.0 class name) in FR-20 instead of generic "recursive character splitting"

---

#### 5. Updated Emergency Escalation (Section 4.5)
**Actions:** Renumbered FR-22 to FR-25 → FR-23 to FR-26

---

#### 6. Updated Session Management (Section 4.6)
**Before:** Generic persistence language

**After:**
- ✅ **FR-28:** "persist conversation history for each session using `InMemorySaver()` from `langgraph.checkpoint.memory`"
- ✅ **FR-30:** "maintain session context across browser refreshes by passing a consistent `thread_id` in the config"

**Rationale:** Specified exact v1.0 classes and patterns for memory management

---

#### 7. Updated LLM Provider Strategy (Section 4.7)
**Before:** Generic "GPT-4 or GPT-4.5"

**After:**
- ✅ **FR-31:** "OpenAI (GPT-4 or GPT-4o-mini): For generating high-quality final responses from specialized agents"
- ✅ **FR-31:** "AWS Bedrock (Claude 3 Haiku or Nova Lite): For fast, cost-effective query routing and classification in the supervisor agent"

**Rationale:** Updated to current OpenAI models and clarified role of each LLM in supervisor pattern

---

#### 8. Updated Vector Database (Section 4.8)
**Actions:** Renumbered FR-33 to FR-37 → FR-34 to FR-38

---

#### 9. Updated API Endpoints (Section 4.9)
**Actions:** Renumbered FR-38 to FR-40 → FR-39 to FR-41

---

#### 10. Updated User Interface (Section 4.10)
**Actions:** Renumbered FR-41 to FR-45 → FR-42 to FR-46

---

#### 11. Completely Rewrote Technology Stack (Section 7.1)

**Before:**
- TC-3: "LangChain 0.1+, LangGraph, LCEL (LangChain Expression Language)"
- TC-4: Generic LLM providers
- TC-5: ChromaDB
- TC-6: pypdf, pdfplumber, python-docx

**After:**
- ✅ **TC-3:** "LangChain v1.0+, LangGraph (for custom orchestration workflows if needed)"
- ✅ **TC-4:** "Agent Architecture: Use `create_agent()` from `langchain.agents` for all agents (supervisor and workers) following the v1.0 supervisor pattern with tool calling"
- ✅ **TC-5:** "LLM Providers: OpenAI API (GPT-4o-mini for agents), AWS Bedrock (Claude 3 Haiku for routing)"
- ✅ **TC-6:** ChromaDB 0.4+
- ✅ **TC-7:** "PyPDFLoader, TextLoader, UnstructuredMarkdownLoader, RecursiveCharacterTextSplitter"
- ✅ **TC-8:** "Memory/State: InMemorySaver() from langgraph.checkpoint.memory for conversation persistence"

**Rationale:** Removed deprecated LCEL, specified v1.0 classes, updated to current model names

---

#### 12. Added New Section: Agent Architecture (Section 7.2)

**New Content:**
- ✅ **TC-9:** LangChain v1.0 supervisor pattern implementation details
  - Create all agents using `create_agent()`
  - Wrap workers as tools with `@tool` decorator
  - Supervisor invokes workers by calling tools
  - Workers include all info in final response
- ✅ **TC-10:** Required parameters for each agent:
  - `name` (descriptive, snake_case)
  - `system_prompt` (emphasizes complete results in final output)
  - `tools` list (RAG tools for workers, agent tools for supervisor)
  - `model` string (e.g., "openai:gpt-4o-mini")
  - `checkpointer` (InMemorySaver() for MVP)
- ✅ **TC-11:** Tools to create with `@tool` decorator:
  - RAG retrieval tools for each knowledge base
  - Agent wrapper tools
  - Emergency escalation detection tools
- ✅ **TC-12:** Manual LangGraph StateGraph only for custom workflow logic (not expected for MVP)

**Rationale:** Provided clear, actionable guidance on v1.0 agent creation

---

#### 13. Replaced LangGraph Workflow with Conversation Flow (Section 7.3)

**Before (Generic Node Structure):**
- TC-8: Listed 7 LangGraph nodes (Input Validation, Orchestrator/Router, Specialized Agents, Retrieval, Response Generation, Response Formatting, History Persistence)
- TC-9: Conditional edges for routing

**After (LangChain v1.0 Supervisor Pattern Flow):**
- ✅ **TC-13:** 7-step conversation flow:
  1. User submits query → FastAPI receives
  2. Supervisor agent invoked with thread_id
  3. Supervisor analyzes using AWS Bedrock
  4. Supervisor calls appropriate worker tool
  5. Worker executes (receives query, calls RAG tool, generates response, returns to supervisor)
  6. Supervisor formats and streams response
  7. Conversation saved with thread_id
- ✅ **TC-14:** Code example showing `.invoke()` method with config:
  ```python
  config = {"configurable": {"thread_id": session_id}}
  result = supervisor_agent.invoke({"messages": [user_message]}, config)
  ```

**Rationale:** Replaced generic nodes with specific v1.0 supervisor pattern flow

---

#### 14. Added New Section: Context Engineering (Section 7.4)

**New Content:**
- ✅ **TC-15:** LangChain v1.0 context engineering patterns
  - **Model Context (Transient):**
    - Dynamic system prompts
    - Inject relevant context
    - Consider `@dynamic_prompt` decorator
  - **Tool Context (Persistent):**
    - Tools use `ToolRuntime` to access state, store, config
    - Use `Command` to update state persistently
    - Pass conversation context via tool parameters
  - **Life-cycle Context:**
    - `@before_model` hooks for validation/safety checks
    - `@after_model` hooks for logging/formatting
    - `SummarizationMiddleware` if conversations exceed token limits

**Rationale:** Introduced v1.0 context engineering patterns for reliable agent behavior

---

#### 15. Updated Error Handling (Section 7.5)
**Actions:** Renumbered TC-10 to TC-11 → TC-16 to TC-17

---

#### 16. Updated Performance Requirements (Section 7.6)
**Actions:** Renumbered TC-12 to TC-15 → TC-18 to TC-21

---

#### 17. Updated Data Persistence (Section 7.7)
**Before:** Generic "persist in memory for active sessions"

**After:**
- ✅ **TC-23:** "Conversation history must persist in memory for active sessions using `InMemorySaver()` from `langgraph.checkpoint.memory`"

**Rationale:** Specified exact v1.0 class for memory persistence

---

#### 18. Updated Configuration (Section 7.8)

**Added Environment Variables:**
- ✅ `LANGSMITH_TRACING` (optional, for development debugging)
- ✅ `LANGSMITH_API_KEY` (optional, for development debugging)
- ✅ `LANGSMITH_PROJECT` (optional, for development debugging)

**Rationale:** LangSmith is strongly recommended in v1.0 guidelines for debugging and monitoring

---

### Summary of LangChain v1.0 Updates

**Deprecated Patterns Removed:**
- ❌ LCEL (LangChain Expression Language) - completely removed
- ❌ Generic "orchestrator agent" language
- ❌ Manual LangGraph node structure (replaced with supervisor pattern)
- ❌ Outdated model references (GPT-4.5)

**v1.0 Patterns Added:**
- ✅ `create_agent()` from `langchain.agents` for all agents
- ✅ Supervisor pattern with tool calling
- ✅ `@tool` decorator for worker agents and RAG tools
- ✅ `InMemorySaver()` for conversation persistence
- ✅ `.invoke()` method with `thread_id` config
- ✅ Context engineering patterns (Model, Tool, Life-cycle)
- ✅ Proper v1.0 document loaders (PyPDFLoader, TextLoader, etc.)
- ✅ RecursiveCharacterTextSplitter
- ✅ LangSmith environment variables
- ✅ Current OpenAI models (GPT-4o-mini)

**New Sections Added:**
1. Agent Architecture (Section 7.2) - detailed v1.0 implementation guide
2. Context Engineering (Section 7.4) - transient and persistent context patterns
3. Conversation Flow (Section 7.3) - replaced generic node structure with supervisor pattern flow

**Total Technical Considerations:**
- Before: TC-1 to TC-22
- After: TC-1 to TC-28 (reorganized and expanded)

---

## Final PRD Statistics

**File:** `/tasks/0001-prd-aerospace-customer-service.md`
**Total Lines:** 553
**Document Version:** 1.0 (LangChain v1.0 Compliant)
**Date Created:** November 1, 2025

### PRD Structure:
1. Introduction/Overview
2. Goals (6 objectives)
3. User Stories (11 stories - internal users only)
4. Functional Requirements (46 requirements across 10 subsections)
5. Non-Goals (11 exclusions)
6. Design Considerations
7. Technical Considerations (8 subsections, 28 technical requirements)
8. Success Metrics (11 metrics)
9. Open Questions (9 answered questions)
10. Development Methodology (Vibe Coding Strategy)
11. Acceptance Criteria (18 criteria)
12. Submission Deliverables
13. Appendix A: Example Queries

### Key Features:
- **Multi-Agent Architecture:** Supervisor pattern with 3 specialized worker agents
- **Retrieval Strategies:** Hybrid RAG/CAG, Pure RAG, Pure CAG
- **Emergency Escalation:** Safety-critical query detection with email escalation
- **Document Management:** Auto-Map and manual knowledge base selection
- **Professional Branding:** "The Aerospace Company Customer Service Agent" with airplane logo
- **LangChain v1.0 Compliant:** Uses `create_agent()`, supervisor pattern, context engineering
- **Internal User Focus:** Designed exclusively for customer service representatives
- **Conversation Persistence:** 3-conversation FIFO retention with InMemorySaver()
- **Dual LLM Strategy:** OpenAI for quality, AWS Bedrock for cost-effective routing

---

## Key Decisions & Rationale

### Decision 1: Internal Users Only
**Rationale:** Simplified scope to focus on representative empowerment rather than direct customer interaction. This allows for MVP development without needing production-grade authentication, customer-facing UI polish, or external support infrastructure.

### Decision 2: Standard Three Agents
**Rationale:** Keeps MVP focused on demonstrating core multi-agent architecture without overcomplicating with aerospace-specific agents. The three agents (Billing, Technical, Policy) provide sufficient diversity to showcase routing and retrieval strategies.

### Decision 3: Customer Satisfaction as Primary Metric
**Rationale:** Aligns with business value - improving customer experience is the ultimate goal. Representative satisfaction and efficiency metrics support this primary objective.

### Decision 4: Auto-Map with Manual Override
**Rationale:** Provides best of both worlds - intelligent automation for efficiency with representative control for accuracy. Default to auto-map reduces friction while manual option ensures flexibility for edge cases.

### Decision 5: FIFO 3-Conversation Retention
**Rationale:** Balances context availability with data management. Three conversations provide sufficient history for representatives to reference recent interactions without overwhelming storage or creating data governance complexity.

### Decision 6: Email Escalation (ski@aerospace-co.com)
**Rationale:** Simple, reliable escalation path appropriate for MVP. Email provides audit trail and doesn't require integration with complex paging/ticketing systems.

### Decision 7: LangChain v1.0 Supervisor Pattern
**Rationale:** Follows current best practices, avoids deprecated LCEL patterns, provides clean, maintainable code with built-in state management and tool calling. Supervisor pattern is simpler than manual LangGraph StateGraph while still being production-ready.

### Decision 8: Dual LLM Strategy
**Rationale:** Cost optimization - AWS Bedrock (Claude Haiku) for frequent routing decisions, OpenAI (GPT-4o-mini) for quality responses. Demonstrates multi-provider architecture and intelligent resource allocation.

### Decision 9: No File Attachments in Chat
**Rationale:** Keeps chat interface clean and focused on conversation. Document management handled through dedicated upload interface with proper categorization and processing pipeline.

### Decision 10: LangSmith Optional for Development
**Rationale:** Strongly recommended for debugging and monitoring agent behavior, but optional to avoid mandatory third-party dependency for MVP. Provides valuable tracing without blocking development.

---

## Implementation Priorities (Based on PRD)

### Phase 1: Foundation (Weeks 1-2)
1. Set up project structure (backend FastAPI, frontend Next.js)
2. Configure environment variables and LangSmith tracing
3. Create ChromaDB collections (billing, technical, policy)
4. Implement document ingestion pipeline with Auto-Map

### Phase 2: Core Agents (Weeks 3-4)
5. Create three worker agents using `create_agent()`
6. Implement RAG retrieval tools for each knowledge base
7. Wrap worker agents as tools with `@tool` decorator
8. Create supervisor agent with tool calling

### Phase 3: API & Integration (Weeks 5-6)
9. Build FastAPI endpoints (chat, upload, collections, sessions, health)
10. Implement Server-Sent Events for streaming responses
11. Add InMemorySaver() for conversation persistence with FIFO
12. Implement emergency escalation detection

### Phase 4: Frontend (Weeks 7-8)
13. Build Next.js chat interface with shadcn/ui
14. Create document upload interface with dropdown and Auto-Map
15. Add "The Aerospace Company Customer Service Agent" branding
16. Implement session management UI

### Phase 5: Testing & Polish (Week 9)
17. User testing with 20+ internal representatives
18. Measure customer satisfaction scores
19. Fix bugs and polish UI/UX
20. Record 5-10 minute demonstration video

---

## Document Change Log

| Date | Version | Changes | Approver |
|------|---------|---------|----------|
| 2025-11-01 | 1.0 Initial | Created initial PRD with external + internal users | User |
| 2025-11-01 | 2.0 Internal Focus | Removed external users, added Auto-Map, answered open questions | User |
| 2025-11-01 | 3.0 v1.0 Compliant | Aligned with LangChain v1.0 best practices, supervisor pattern | User |

---

## Next Steps

1. ✅ **Review PRD** - User approved final version
2. ⏭️ **Set up development environment** - Create project structure
3. ⏭️ **Create mock aerospace data** - Public FAA documents + synthetic data
4. ⏭️ **Begin Phase 1 implementation** - Document ingestion pipeline
5. ⏭️ **Enable LangSmith tracing** - For development debugging

---

## Appendix: All User Responses Summary

| Question | User Response | Impact on PRD |
|----------|---------------|---------------|
| Q1: Problem/Goal | D (All of the above) | Comprehensive goals covering response time, accuracy, scaling |
| Q2: Target Users | C (Both external + internal) → Modified to internal only | Focus shifted to internal representatives exclusively |
| Q3: Agent Specializations | F (Standard three agents) | Kept MVP simple with Billing, Technical, Policy agents |
| Q4: Data Sources | E (All of the above) | Support for manuals, compliance docs, parts catalogs, contracts |
| Q5: Success Criteria | C (Customer satisfaction) | Primary metric: 4.0/5.0 satisfaction score |
| Q6: Scope Boundaries | C,D (Voice + Auth excluded) | Added to Non-Goals, kept MVP text-based with basic auth |
| Q7: Critical Edge Cases | B (Emergency escalation) | Implemented safety-critical detection + email escalation |
| OQ-1: Satisfaction Collection | In-app survey | Survey after conversation or 5+ messages |
| OQ-2: Logging Policy | Last 3 conversations, FIFO | FIFO retention for 3 conversations per representative |
| OQ-3: KB Update Process | Admin upload | Document upload interface by authorized reps |
| OQ-4: User Permissions | Internal only | Removed all external user features |
| OQ-5: Escalation Contact | ski@aerospace-co.com | Email escalation throughout document |
| OQ-6: Industry Certifications | No | Added to Non-Goals |
| OQ-7: File Attachments | No | Added to Non-Goals, dedicated upload interface only |
| OQ-8: Document Volume | 100 files/collection, 100KB avg | System designed for ~10MB per collection |
| OQ-9: Mock Data | Public FAA + synthetic | Noted for demo/testing purposes |

---

**Document Compiled By:** AI Assistant (Claude Sonnet 4.5)  
**Compilation Date:** November 1, 2025  
**PRD File Location:** `/tasks/0001-prd-aerospace-customer-service.md`  
**Total Conversations:** 3  
**Total User Responses Captured:** 16  
**Total Actions/Changes:** 75+

