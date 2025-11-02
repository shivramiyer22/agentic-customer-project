# Troubleshooting Guide

## Issue: Next.js Lock File Preventing Server Start

### Error Message:
```
⨯ Unable to acquire lock at .next/dev/lock, is another instance of next dev running?
```

### Root Cause:
When Next.js dev server doesn't shut down cleanly (e.g., process killed abruptly), it leaves behind a lock file in `.next/dev/lock` that prevents new instances from starting.

### Fix:
1. **Kill all node processes:**
   ```bash
   killall node
   ```

2. **Remove the lock file and clear cache:**
   ```bash
   cd frontend
   rm -rf .next
   rm -rf node_modules/.cache
   ```

3. **Restart the server:**
   ```bash
   npm run dev
   ```

### Prevention:
- Always use `Ctrl+C` to gracefully stop the dev server
- If a process is stuck, kill it first before starting a new one

---

## Issue: 404 Error on Chat Endpoint

### Error Message:
```
POST http://localhost:8000/chat 404 (Not Found)
```

### Root Cause:
The backend server doesn't have a `/chat` endpoint defined to handle POST requests for chat messages.

### Fix:
1. **Create the chat router** at `backend/app/routers/chat.py`:
   - Define `POST /chat` endpoint
   - Support both streaming (SSE) and non-streaming responses
   - Accept `session_id`, `message`, and `stream` flag

2. **Register the router** in `backend/app/main.py`:
   ```python
   from app.routers import chat
   app.include_router(chat.router)
   ```

3. **Restart the backend server:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Notes:
- The chat endpoint uses Server-Sent Events (SSE) for streaming responses
- Currently returns placeholder responses until agent system is implemented
- Endpoint accepts: `{ session_id: string, message: string, stream: boolean }`

---

## Issue: 404 Error on Sessions Endpoint

### Error Message:
```
GET http://localhost:8000/sessions 404 (Not Found)
```

### Root Cause:
The backend server doesn't have a `/sessions` endpoint defined.

### Fix:
1. **Create the sessions router** at `backend/app/routers/sessions.py`:
   - `GET /sessions` - List all sessions
   - `GET /sessions/{session_id}` - Get specific session
   - `POST /sessions` - Create new session
   - `DELETE /sessions/{session_id}` - Delete session

2. **Register the router** in `backend/app/main.py`:
   ```python
   from app.routers import sessions
   app.include_router(sessions.router)
   ```

3. **Restart the backend server**

### Notes:
- Uses in-memory session store for MVP
- Replace with database in production
- Sessions tracked with `created_at`, `updated_at`, `message_count`, and `agent`

---

## Additional Notes:
- The `.next` directory contains build artifacts and lock files
- Clearing it forces Next.js to rebuild from scratch
- This is safe and won't affect your source code

