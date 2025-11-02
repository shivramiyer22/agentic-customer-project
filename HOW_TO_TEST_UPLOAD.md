# How to Test Document Upload for Ingestion

## ✅ Application Status

Both servers are **running**:
- ✅ **Backend API:** http://localhost:8000 (uvicorn process active)
- ✅ **Frontend:** http://localhost:3000 (Next.js server active)
- ✅ **Environment:** Configured with OpenAI API key

---

## 🚀 Quick Start: Test Document Upload

### Method 1: Web Interface (Easiest)

#### Step 1: Open Upload Page
Navigate to: **http://localhost:3000/upload**

#### Step 2: Select Knowledge Base
Use the dropdown to select:
- **Auto-Map** (default) - Automatically categorizes documents based on content
- **Billing Knowledge Base** - For invoices, contracts, pricing documents
- **Technical Knowledge Base** - For manuals, bug reports, specifications
- **Policy Knowledge Base** - For regulations, policies, compliance docs

#### Step 3: Upload Documents
Two ways to upload:
1. **Click Upload Area:** Click the upload box and select files
2. **Drag & Drop:** Drag files onto the upload area

**Supported Formats:**
- ✅ PDF (.pdf)
- ✅ Text (.txt)
- ✅ Markdown (.md)
- ✅ JSON (.json)

**File Size Limit:** ~100 KB per file

#### Step 4: Monitor Progress
Watch for:
- ✅ Upload progress percentage
- ✅ Per-file status updates
- ✅ Chunks count after completion
- ✅ Success/error status for each file

#### Step 5: Verify Success
Check:
- ✅ Files show "success" status
- ✅ Chunks count displayed (e.g., "5 chunks")
- ✅ Target collection shown correctly
- ✅ No error messages

---

### Method 2: Create Test Documents First

#### Create Sample Documents

**1. Billing Document (test_invoice.txt):**
```bash
cd ~/Desktop/SKI\ -\ ASU/Vibe-Coding/agentic-customer-project
cat > test_invoice.txt << 'EOF'
Invoice #12345
Customer: Test Aerospace Corp
Date: 2025-01-15
Amount: $10,000.00

Items:
- Part A123: $5,000.00
- Part B456: $5,000.00

Payment Terms: Net 30
Contract: C-2024-001
EOF
```

**2. Technical Document (test_manual.txt):**
```bash
cat > test_manual.txt << 'EOF'
Technical Manual: System XYZ
Version: 2.0

Installation:
1. Unpack files
2. Run setup.sh
3. Configure database

Troubleshooting:
- Error 404: Check database connection
- Error 500: Verify file permissions

Specifications:
- CPU: 4 cores minimum
- RAM: 8GB minimum
EOF
```

**3. Policy Document (test_policy.txt):**
```bash
cat > test_policy.txt << 'EOF'
Policy Document: Data Governance
Effective Date: 2025-01-01

Compliance Requirements:
- GDPR compliance for EU customers
- CCPA compliance for California customers
- DFARs compliance for government contracts

Data Retention: 7 years
Security: Encryption at rest and in transit
EOF
```

#### Upload Test Documents

1. Go to **http://localhost:3000/upload**
2. Select **"Auto-Map"** to test automatic categorization
3. Upload all three test files
4. Watch them get categorized automatically:
   - `test_invoice.txt` → Should map to `billing_knowledge_base`
   - `test_manual.txt` → Should map to `technical_knowledge_base`
   - `test_policy.txt` → Should map to `policy_knowledge_base`

---

### Method 3: API Direct (curl)

#### Upload Single File

```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@test_invoice.txt" \
  -F "target_collection=auto-map"
```

**Response:**
```json
{
  "upload_id": "abc123...",
  "status": "queued",
  "files": [
    {
      "file_name": "test_invoice.txt",
      "file_size": 456,
      "status": "queued",
      "progress": 0.0
    }
  ],
  "overall_progress": 0.0,
  "created_at": "2025-01-15T10:00:00"
}
```

#### Upload Multiple Files

```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@test_invoice.txt" \
  -F "files=@test_manual.txt" \
  -F "files=@test_policy.txt" \
  -F "target_collection=auto-map"
```

#### Check Upload Status

```bash
# Replace {upload_id} with ID from upload response
curl http://localhost:8000/upload/status/{upload_id}
```

---

## ✅ Verification Steps

### 1. Check Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "chromadb": {
    "connected": true,
    "collections_count": 3,
    "collections": [
      "billing_knowledge_base",
      "technical_knowledge_base",
      "policy_knowledge_base"
    ]
  },
  "timestamp": "2025-01-15T10:00:00"
}
```

### 2. Check Collections Endpoint

```bash
curl http://localhost:8000/collections
```

**Expected:**
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

### 3. Verify in Web UI

In the upload page:
- ✅ Files show "success" status
- ✅ Chunks count displayed (e.g., "5 chunks")
- ✅ Target collection shown
- ✅ No error messages

---

## 🧪 Testing Auto-Map Feature

The **Auto-Map** feature analyzes document content and automatically categorizes:

| Document Type | Keywords | Maps To |
|--------------|----------|---------|
| **Billing** | invoice, payment, contract, pricing, billing | `billing_knowledge_base` |
| **Technical** | installation, troubleshooting, manual, specification, bug | `technical_knowledge_base` |
| **Policy** | policy, compliance, regulation, governance, requirement | `policy_knowledge_base` |

### Test Auto-Map

1. Select **"Auto-Map"** in dropdown
2. Upload test documents (invoice, manual, policy)
3. Watch them get categorized automatically
4. Verify `target_collection` in upload status

---

## 📊 Expected Upload Flow

### 1. File Selection
- Files appear in preview list
- Status: "pending"

### 2. Upload Process
- Status: "uploading"
- Progress percentage increases
- Real-time updates via polling

### 3. Ingestion Process
- Status: "processing"
- File parsed (PDF, TXT, MD, JSON)
- Content chunked
- Embeddings generated
- Documents stored in ChromaDB

### 4. Completion
- Status: "success"
- Chunks count displayed
- Target collection shown
- Documents ready for retrieval

---

## 🔍 Troubleshooting

### Upload Fails

**Check:**
1. File size ≤ 100 KB
2. File format supported (PDF, TXT, MD, JSON)
3. Backend server running (http://localhost:8000)
4. Backend logs for errors

**Common Issues:**
- File too large → Reduce file size
- Unsupported format → Convert to PDF/TXT
- ChromaDB error → Check database connection
- OpenAI API error → Check API key and quota

### Documents Not Appearing

**Verify:**
1. Upload completed successfully
2. ChromaDB connected (check `/health` endpoint)
3. Collections exist (check `/collections` endpoint)
4. No errors in backend logs

---

## 📝 Test Checklist

Use this checklist to verify upload functionality:

- [ ] Can access http://localhost:3000/upload
- [ ] Can select knowledge base from dropdown
- [ ] Can select files (click or drag-drop)
- [ ] Files appear in preview list
- [ ] Upload button works
- [ ] Progress updates in real-time
- [ ] Files show "success" status after upload
- [ ] Chunks count displayed correctly
- [ ] Target collection shown correctly
- [ ] Collections endpoint shows 3 collections
- [ ] Health endpoint shows ChromaDB connected
- [ ] Auto-Map categorizes documents correctly

---

## 🎯 Quick Reference

| Action | URL | Method |
|--------|-----|--------|
| **Upload Page** | http://localhost:3000/upload | Browser |
| **Chat Interface** | http://localhost:3000 | Browser |
| **API Docs** | http://localhost:8000/docs | Browser |
| **Health Check** | http://localhost:8000/health | GET |
| **Collections** | http://localhost:8000/collections | GET |
| **Upload API** | http://localhost:8000/upload | POST |
| **Upload Status** | http://localhost:8000/upload/status/{id} | GET |

---

## 🚀 Ready to Test?

**Start here:** **http://localhost:3000/upload**

1. Select "Auto-Map" from dropdown
2. Upload test documents
3. Watch automatic categorization
4. Verify success in UI

---

## 💡 Tips

- **Start with Auto-Map** to test automatic categorization
- **Use small test files** (< 100 KB) for quick testing
- **Check backend logs** if upload fails (Terminal 1)
- **Check browser console** for frontend errors
- **Use API Docs** (http://localhost:8000/docs) for detailed API testing

---

**Need Help?**
- Backend logs: Check Terminal 1 (backend)
- Frontend console: Check browser DevTools
- API documentation: http://localhost:8000/docs

