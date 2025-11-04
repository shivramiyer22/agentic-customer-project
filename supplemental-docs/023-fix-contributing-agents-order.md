# Fix: Contributing Agents Order and Accuracy

**Date**: November 2, 2025  
**Issue**: Contributing Agents field was displaying incorrect order and count

## Problem Description

The Contributing Agents and Contributing Models fields were not being computed correctly:

1. **Order was wrong**: Agents were not displayed in the sequence they were invoked
2. **Count was wrong**: Same agent could appear multiple times or be missing
3. **Persistence issue**: Values from previous requests were leaking into new requests

## Root Causes

### Backend Issue
The streaming logic in `backend/app/routers/chat.py` was **re-processing all messages in every chunk**, not just new ones. This caused:
- Tool calls to be detected multiple times
- Order to be scrambled as messages were re-scanned
- The duplicate check (`not in contributing_agents`) masked the real issue but didn't fix ordering

### Frontend Issue
When creating placeholder assistant messages, the `contributingAgents` and `contributingModels` fields were not explicitly cleared, causing values from previous responses (stored in localStorage) to persist.

## Solution

### Backend Fix (`backend/app/routers/chat.py`)

1. **Track processed messages**: Added `processed_message_ids = set()` to track which messages have already been analyzed
2. **Skip duplicate processing**: Check `if msg_id in processed_message_ids: continue` before processing each message
3. **Remove duplicate check**: Since we only process each message once, removed the `not in contributing_agents` check
4. **Preserve invocation order**: Agents are now appended in the exact order their tool_calls appear

```python
# Track which messages we've already processed
processed_message_ids = set()

for msg in messages:
    msg_id = id(msg)  # Python's id() for object identity
    
    # Skip if already processed
    if msg_id in processed_message_ids:
        continue
    
    processed_message_ids.add(msg_id)
    
    # Process tool_calls - append in order
    if agent_name:
        contributing_agents.append(agent_name)  # No duplicate check needed
```

### Frontend Fixes

#### 1. Clear placeholder values (`frontend/src/hooks/useChat.ts`)
```typescript
// Add placeholder with empty arrays
addMessage({
  role: 'assistant',
  content: '',
  contributingAgents: [],  // ← Explicitly clear
  contributingModels: [],  // ← Explicitly clear
});
```

#### 2. Always update arrays (`frontend/src/context/ChatContext.tsx`)
```typescript
// Always update, even if empty (to clear previous values)
const updatedMessage = { 
  ...lastMessage, 
  content: updatedContent,
  contributingAgents: contributingAgents || [],  // Always set
  contributingModels: contributingModels || []   // Always set
};
```

#### 3. Remove length checks (`frontend/src/context/ChatContext.tsx`)
```typescript
// Allow empty arrays to clear values
if (lastMessage && lastMessage.role === 'assistant') {
  return [...prev.slice(0, -1), { ...lastMessage, contributingAgents }];
}
// Removed: && contributingAgents.length > 0
```

## Expected Behavior After Fix

For a query like: "How many high priority bugs were resolved this year, what is the SLA level for resolution?"

### Correct Output:
```
Contributing Agents: Technical Support Agent, Policy & Compliance Agent
Contributing Models: AWS Bedrock Claude 3 Haiku, OpenAI gpt-4o-mini, OpenAI gpt-4o-mini
```

### Order Explanation:
1. Supervisor agent analyzes query → AWS Bedrock Claude 3 Haiku
2. Calls Technical Support Agent first → OpenAI gpt-4o-mini
3. Calls Policy & Compliance Agent second → OpenAI gpt-4o-mini
4. Final response synthesizes results

## Testing

### Manual Test
1. Clear browser localStorage: `localStorage.clear()`
2. Send query: "How many high priority bugs were resolved this year, what is the SLA level?"
3. Verify Contributing Agents shows both agents in correct order
4. Send another query: "What is the billing policy?"
5. Verify Contributing Agents resets and shows only "Policy & Compliance Agent"

### Verification Points
- [ ] Contributing Agents resets for each new query
- [ ] Agents appear in invocation order (left to right)
- [ ] No duplicate agents in the list
- [ ] Contributing Models matches agents (supervisor + worker agents)
- [ ] Order is preserved across page navigation (localStorage)

## Files Modified

1. `backend/app/routers/chat.py` - Message processing logic
2. `frontend/src/hooks/useChat.ts` - Placeholder message initialization
3. `frontend/src/context/ChatContext.tsx` - State update logic

## Related Issues

- Previous fix: Contributing Agents/Models display formatting (same line with `||` separator)
- Previous fix: Chat history persistence with localStorage
- Previous fix: Hydration mismatch error

## Notes

- The `id()` function in Python returns the memory address of an object, which is unique for each message instance
- This approach is more reliable than trying to track message indices or timestamps
- The supervisor model is always added first since it's invoked before any worker agents




