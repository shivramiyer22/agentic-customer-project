# How to Run the Application and Test Document Upload

## Quick Start Guide

### Prerequisites Check

Ensure you have:
- ✅ Python 3.11+ installed
- ✅ Node.js 18.x+ and npm installed
- ✅ OpenAI API key (already configured in `backend/.env`)

---

## Step 1: Start the Backend Server

Open **Terminal 1**:

```bash
# Navigate to backend directory
cd /Users/manasaiyer/Desktop/SKI\ -\ ASU/Vibe-Coding/agentic-customer-project/backend

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **Backend is running at:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Step 2: Start the Frontend Server

Open **Terminal 2** (new terminal window):

```bash
# Navigate to frontend directory
cd /Users/manasaiyer/Desktop/SKI\ -\ ASU/Vibe-Coding/agentic-customer-project/frontend

# Start Next.js development server
npm run dev
```

**Expected Output:**
```
▲ Next.js 16.0.1
- Local:        http://localhost:3000
```

✅ **Frontend is running at:** http://localhost:3000

---

## Step 3: Access the Application

Open your web browser and navigate to:

1. **Main Chat Interface:** http://localhost:3000
2. **Document Upload Page:** http://localhost:3000/upload
3. **Backend API Docs:** http://localhost:8000/docs

---

## Step 4: Test Document Upload for Ingestion

### Option A: Using the Web Interface (Recommended)

1. **Navigate to Upload Page**
   - Go to: http://localhost:3000/upload
   - Or click the upload link in the main interface

2. **Select Knowledge Base** (Optional)
   - Choose from dropdown:
     - **Auto-Map** (default) - Automatically categorizes documents
     - **Billing Knowledge Base** - For invoices, contracts, pricing
     - **Technical Knowledge Base** - For manuals, bug reports, specs
     - **Policy Knowledge Base** - For regulations, policies, compliance

3. **Upload Documents**
   - **Method 1:** Click the upload area and select files
   - **Method 2:** Drag and drop files onto the upload area
   - Supported formats: **PDF, TXT, Markdown (.md), JSON**
   - Maximum file size: **100 KB per file** (target)

4. **Monitor Upload Progress**
   - View real-time progress for each file
   - See chunk count after successful upload
   - Check for any errors

5. **Verify Upload Success**
   - Files should show "success" status
   - Chunks count should be displayed
   - No error messages

### Option B: Using the API Directly

You can also test upload via the API using `curl` or Postman:

```bash
# Upload a single file
curl -X POST http://localhost:8000/upload \
  -F "files=@/path/to/your/document.pdf" \
  -F "target_collection=auto-map"

# Upload multiple files
curl -X POST http://localhost:8000/upload \
  -F "files=@/path/to/document1.pdf" \
  -F "files=@/path/to/document2.txt" \
  -F "target_collection=billing_knowledge_base"
```

**Check Upload Status:**
```bash
# Replace {upload_id} with the ID from the upload response
curl http://localhost:8000/upload/status/{upload_id}
```

---

## Step 5: Verify Documents Are Ingested

### Check Collections Endpoint

```bash
curl http://localhost:8000/collections
```

Should return:
```json
{
  "collections": [
    "billing_knowledge_base",
    "technical_knowledge_base",
    "policy_knowledge_base"
  ],
  "configured": [...],
  "count": 3
}
```

### Check Health Endpoint

```bash
curl http://localhost:8000/health
```

Should show ChromaDB is connected and collections are initialized.

---

## Testing with Sample Documents

### Create Test Documents

Create test files in your project directory:

**For Billing Knowledge Base:**
```bash
# Create a sample invoice
echo "Invoice #12345
Customer: Test Corp
Amount: \$1,000.00
Date: 2025-01-15
Items:
- Part A: \$500.00
- Part B: \$500.00" > test_invoice.txt
```

**For Technical Knowledge Base:**
```bash
# Create a sample technical document
echo "Technical Manual: System X
Version: 1.0
Description: This system handles...
Installation: Follow steps 1-5
Troubleshooting: See section 4" > test_manual.txt
```

**For Policy Knowledge Base:**
```bash
# Create a sample policy document
echo "Policy Document: Data Governance
Effective Date: 2025-01-01
Scope: All customer data
Compliance: GDPR, CCPA
Requirements: See section 3" > test_policy.txt
```

### Upload Test Documents

1. Go to http://localhost:3000/upload
2. Select "Auto-Map" or choose a specific knowledge base
3. Upload your test files
4. Wait for upload to complete
5. Verify chunks are created (shown in the UI)

---

## Expected Behavior

### Successful Upload Flow

1. **File Selection**
   - Files appear in the preview list
   - Status shows "pending"

2. **Upload Process**
   - Status changes to "uploading"
   - Progress percentage increases
   - Real-time updates via polling

3. **Completion**
   - Status changes to "success"
   - Chunks count displayed (e.g., "5 chunks")
   - File categorized to appropriate knowledge base

4. **Auto-Map Behavior**
   - System analyzes document content
   - Categorizes to: billing, technical, or policy
   - Based on keywords and content analysis

---

## Troubleshooting

### Upload Fails

1. **Check File Size**
   - Maximum: 100 KB per file
   - Check file size before upload

2. **Check File Format**
   - Supported: PDF, TXT, MD, JSON
   - Verify file extension matches format

3. **Check Backend Logs**
   - Look for errors in Terminal 1 (backend)
   - Common issues: ChromaDB connection, OpenAI API errors

4. **Check Network**
   - Verify frontend can reach backend
   - Check CORS settings if seeing 401/403 errors

### Documents Not Appearing

1. **Verify ChromaDB**
   ```bash
   curl http://localhost:8000/health
   ```
   Should show ChromaDB is connected

2. **Check Collection Status**
   ```bash
   curl http://localhost:8000/collections
   ```
   Verify collections exist

3. **Check Backend Logs**
   - Look for ingestion errors
   - Check OpenAI API quota/rate limits

---

## Next Steps After Upload

Once documents are uploaded:

1. **Test Chat Interface**
   - Go to http://localhost:3000
   - Ask questions related to uploaded documents
   - Verify agents can retrieve information

2. **Test Knowledge Base Queries**
   - Try billing-related questions → should route to Billing Agent
   - Try technical questions → should route to Technical Agent
   - Try policy questions → should route to Policy Agent

---

## Quick Reference

| Service | URL | Status Check |
|---------|-----|--------------|
| Backend API | http://localhost:8000 | http://localhost:8000/health |
| Frontend | http://localhost:3000 | http://localhost:3000 |
| Upload Page | http://localhost:3000/upload | Visual UI |
| API Docs | http://localhost:8000/docs | Swagger UI |

---

## Test Upload Checklist

- [ ] Backend server is running (Terminal 1)
- [ ] Frontend server is running (Terminal 2)
- [ ] Can access http://localhost:3000/upload
- [ ] Can select knowledge base from dropdown
- [ ] Can select files (PDF, TXT, MD, JSON)
- [ ] Upload progress shows correctly
- [ ] Files show "success" status after upload
- [ ] Chunks count is displayed
- [ ] Collections endpoint shows updated count
- [ ] Health endpoint shows ChromaDB connected

---

**Need Help?** Check:
- Backend logs in Terminal 1
- Frontend console in browser DevTools
- API documentation at http://localhost:8000/docs

