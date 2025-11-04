# Backend Testing Guide

## Overview

This directory contains comprehensive tests for the backend application, organized according to FastAPI best practices.

## Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── test_main.py             # Tests for main FastAPI application
├── test_config.py           # Tests for configuration module
├── test_routers_health.py   # Tests for health router
├── test_routers_collections.py  # Tests for collections router
├── test_routers_upload.py  # Tests for upload router
├── test_routers_chat.py    # Tests for chat router (Task 5.0)
├── test_state.py           # Tests for conversation state (Task 5.0)
├── test_schemas_chat.py    # Tests for chat schemas (Task 5.0)
├── test_agents_orchestrator.py  # Tests for supervisor agent (Task 5.0)
├── test_cag_retriever.py   # Tests for CAG retrieval (Task 6.0)
├── test_policy_agent.py    # Tests for policy agent (Task 6.0)
├── test_policy_agent_integration.py  # Tests for policy agent integration (Task 6.0)
├── test_rag_retriever.py   # Tests for RAG retrieval (Task 7.0)
├── test_technical_agent.py    # Tests for technical agent (Task 7.0)
├── test_technical_agent_integration.py  # Tests for technical agent integration (Task 7.0)
├── test_hybrid_retriever.py   # Tests for Hybrid RAG/CAG retrieval (Task 8.0)
├── test_billing_agent.py    # Tests for billing agent (Task 8.0)
├── test_billing_agent_integration.py  # Tests for billing agent integration (Task 8.0)
├── test_multi_agent_routing.py  # Tests for complete multi-agent system routing (Task 8.0)
├── test_parsers.py          # Tests for document parsers
├── test_chunkers.py         # Tests for document chunkers
├── test_chroma_client.py    # Tests for ChromaDB client
├── test_ingestion_comprehensive.py  # Comprehensive ingestion tests
├── test_integration.py      # Integration tests
├── test_connections.py      # Connection tests (OpenAI, AWS Bedrock)
└── test_chromadb_setup.py   # ChromaDB setup verification script
```

## Running Tests

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests

```bash
# From backend directory
cd backend
pytest tests/

# Or from project root
cd /path/to/project
pytest backend/tests/
```

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/test_config.py tests/test_parsers.py

# Router tests
pytest tests/test_routers_*.py

# Integration tests
pytest tests/test_integration.py
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ --cov=app --cov-report=html
```

## Test Categories

### Unit Tests
- **test_config.py**: Configuration validation and defaults
- **test_parsers.py**: Document parser functionality
- **test_chunkers.py**: Text chunking functionality
- **test_chroma_client.py**: ChromaDB client operations
- **test_state.py**: Conversation state management (InMemorySaver)
- **test_schemas_chat.py**: Chat schemas (ChatMessage, ChatResponse, ChatStreamChunk)
- **test_agents_orchestrator.py**: Supervisor agent and tools (includes AWS Bedrock connection tests)
- **test_cag_retriever.py**: CAG retrieval for policy documents (Task 6.0)
- **test_policy_agent.py**: Policy & Compliance Agent (Task 6.0)
- **test_rag_retriever.py**: RAG retrieval for technical documents (Task 7.0)
- **test_technical_agent.py**: Technical Support Agent (Task 7.0)
- **test_hybrid_retriever.py**: Hybrid RAG/CAG retrieval for billing documents (Task 8.0)
- **test_billing_agent.py**: Billing Support Agent (Task 8.0)

### Integration Tests
- **test_routers_*.py**: API endpoint tests (health, collections, upload, chat)
- **test_ingestion_comprehensive.py**: Complete ingestion pipeline
- **test_integration.py**: End-to-end workflows
- **test_policy_agent_integration.py**: Policy agent integration with supervisor (Task 6.0)
- **test_technical_agent_integration.py**: Technical agent integration with supervisor (Task 7.0)
- **test_billing_agent_integration.py**: Billing agent integration with supervisor (Task 8.0)
- **test_multi_agent_routing.py**: Complete multi-agent system routing tests (Task 8.0)

## Test Coverage

The test suite covers:
- ✅ Configuration management
- ✅ API endpoints (health, collections, upload, chat)
- ✅ Document parsing (PDF, TXT, Markdown, JSON)
- ✅ Text chunking
- ✅ ChromaDB operations
- ✅ File validation
- ✅ Document categorization (Auto-Map)
- ✅ Metadata enrichment
- ✅ Error handling
- ✅ Integration workflows
- ✅ Supervisor Agent (Orchestrator)
- ✅ Conversation state management
- ✅ Chat schemas (ChatMessage, ChatResponse, ChatStreamChunk)
- ✅ Emergency detection tools
- ✅ Policy & Compliance Agent (Pure CAG)
- ✅ CAG retrieval implementation (search_policy_kb)
- ✅ Policy agent integration with supervisor
- ✅ Technical Support Agent (Pure RAG)
- ✅ RAG retrieval implementation (search_technical_kb)
- ✅ Technical agent integration with supervisor
- ✅ Billing Support Agent (Hybrid RAG/CAG)
- ✅ Hybrid RAG/CAG retrieval implementation (search_billing_kb, get_cached_policy_info)
- ✅ Billing agent integration with supervisor
- ✅ Complete multi-agent system routing
- ✅ Contributing models tracking (supervisor + worker agents)
- ✅ AWS Bedrock connection verification

## Environment Setup

Tests require:
- Python 3.12+
- OpenAI API key (set in `.env` or environment)
- ChromaDB (local persistence)

## Notes

- Some tests require ChromaDB to be running
- Upload tests create temporary files
- Integration tests may require valid API keys
- Test data is cleaned up automatically using fixtures

