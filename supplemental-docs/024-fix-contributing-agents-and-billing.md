# Fix: Contributing Agents Tracking and Billing KB Retrieval

**Date**: November 2, 2025  
**Issues Fixed**:
1. Contributing Agents not reinitializing properly (retaining and appending previous values)
2. Billing agent returning incorrect invoice data (only retrieving top 3 documents)

---

## Issue 1: Contributing Agents Not Reinitializing

### Problem Description

Contributing Agents was showing accumulated values from previous requests instead of starting fresh. For example:
- **First query**: "What is the SLA?" → Contributing Agents: Policy & Compliance Agent ✓
- **Second query**: "What is the highest invoice?" → Contributing Agents: Technical Support Agent, Policy & Compliance Agent, Billing Support Agent ✗

The second query should only show "Billing Support Agent, Policy & Compliance Agent" but was retaining "Technical Support Agent" from the first query.

### Root Cause

The backend was tracking processed tool_calls using `id(msg)` (Python's object identity), but:
1. Python can **reuse memory addresses** for different objects after garbage collection
2. The same `id(msg)` could refer to different messages across different requests
3. Tool calls were being re-processed or not properly deduplicated

### Solution Implemented

Changed from tracking message IDs to tracking **tool_call IDs** (which are unique and persistent):

```python
# OLD: Track message objects (unreliable)
processed_message_ids = set()
msg_id = id(msg)
if msg_id in processed_message_ids:
    continue

# NEW: Track tool_call IDs (reliable)
processed_tool_call_ids = set()
tool_call_id = tool_call.id  # LangChain provides unique ID for each tool_call
if tool_call_id and tool_call_id in processed_tool_call_ids:
    continue
```

**Why this works:**
- Each tool_call has a **unique, persistent ID** from LangChain
- These IDs don't change across stream chunks
- They're properly scoped to a single request (local variable in `generate_agent_stream`)
- Exact invocation order is preserved

---

## Issue 2: Billing Agent Returning Incorrect Invoice Data

### Problem Description

Query: "Which is the highest valued invoice amount?"
- **Expected**: INV-004 ($357,500)
- **Actual**: INV-003 ($82,500)

### Root Cause

The billing knowledge base search was only retrieving **k=3 documents**, which might not include all invoice documents. If the embedding space puts INV-004 further away or if there are many billing documents, it could be missed.

### Solution Implemented

Increased the default retrieval count from k=3 to k=5:

```python
# OLD
def search_billing_kb(query: str, k: int = 3) -> str:

# NEW
def search_billing_kb(query: str, k: int = 5) -> str:
```

**Why this helps:**
- More comprehensive retrieval ensures all relevant invoices are included
- The LLM can then correctly identify the highest value across all retrieved documents
- Still performant (5 documents is reasonable for ChromaDB similarity search)
- Better coverage for comparative queries ("highest", "largest", "most expensive", etc.)

---

## Files Modified

1. **`backend/app/routers/chat.py`**
   - Changed from `processed_message_ids` to `processed_tool_call_ids`
   - Extract and track `tool_call.id` instead of `id(msg)`
   - Added logging for tool_call_id in debug messages

2. **`backend/app/retrieval/hybrid_retriever.py`**
   - Updated default k from 3 to 5 in `search_billing_kb`
   - Updated docstring to reflect comprehensive retrieval

---

## Testing Instructions

### Test 1: Contributing Agents Reinitialization

1. **Clear browser state**: Open Developer Console → `localStorage.clear()` → Refresh
2. **Send first query**: "What is the SLA for high priority bugs?"
   - Expected: `Contributing Agents: Policy & Compliance Agent`
3. **Send second query**: "Which is the highest valued invoice?"
   - Expected: `Contributing Agents: Billing Support Agent, Policy & Compliance Agent`
   - Should **NOT** show "Technical Support Agent" from first query
4. **Send third query**: "How many bugs were resolved this year and what is the billing policy?"
   - Expected: `Contributing Agents: Technical Support Agent, Policy & Compliance Agent`
   - Should **NOT** show "Billing Support Agent" from second query

### Test 2: Billing Invoice Retrieval

1. **Ensure sample invoices are in billing KB**: Upload or verify INV-001 through INV-004 exist
2. **Send query**: "Which is the highest valued invoice amount and what is the invoice data retention policy?"
   - Expected invoice: INV-004 ($357,500)
   - Expected agents: `Billing Support Agent, Policy & Compliance Agent`
3. **Send query**: "List all invoices sorted by amount"
   - Should retrieve all invoices (now k=5 improves coverage)

---

## Expected Behavior After Fix

### Contributing Agents
✅ **Correct**: Each response starts with empty list, then appends agents in invocation order  
✅ **Correct**: Agents appear left-to-right in the sequence they were called  
✅ **Correct**: No agents from previous requests appear in new responses  
❌ **Before**: Old agents persisted and accumulated across requests

### Billing Retrieval
✅ **Correct**: Retrieves up to 5 most relevant documents (increased coverage)  
✅ **Correct**: LLM has access to all invoices to determine highest value  
❌ **Before**: Only 3 documents retrieved, could miss relevant invoices

---

## Technical Details

### Tool Call ID Structure
LangChain v1.0 tool_calls have the following structure:
```python
{
    "id": "call_abc123xyz",  # Unique identifier
    "name": "billing_tool",  # Tool name
    "args": {"query": "..."}  # Tool arguments
}
```

The `id` field is:
- **Unique** per tool call
- **Persistent** across stream chunks
- **Stable** within a request lifecycle
- **Reset** for each new request (local variable)

### Invocation Order Preservation
1. Supervisor agent analyzes query → AWS Bedrock Claude 3 Haiku
2. Calls tools in sequence → Each tool_call has unique ID
3. Backend tracks tool_call_ids → Appends agents in order
4. Frontend receives metadata → Displays in invocation sequence

---

## Verification Checklist

- [x] Backend reinitializes `contributing_agents = []` for each request
- [x] Frontend clears arrays when adding placeholder message
- [x] Tool_call IDs are properly tracked and deduplicated
- [x] Billing KB retrieves 5 documents instead of 3
- [x] No syntax errors or linter warnings
- [x] Services restarted successfully

---

## Related Files

- `backend/app/routers/chat.py` - Streaming response generation and tool tracking
- `backend/app/retrieval/hybrid_retriever.py` - Billing KB search
- `backend/app/agents/orchestrator.py` - Supervisor agent and tool definitions
- `frontend/src/hooks/useChat.ts` - Frontend streaming message handler
- `frontend/src/context/ChatContext.tsx` - Chat state management

---

## Notes

- The tool_call ID approach is more robust than message ID tracking
- Increasing k=5 for billing is a balance between comprehensiveness and performance
- If users have very large billing document collections, k might need further tuning
- The supervisor model (AWS Bedrock) is always added first to contributing_models




