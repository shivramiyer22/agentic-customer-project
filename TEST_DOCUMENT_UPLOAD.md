# How to Test Document Upload for Ingestion

## ✅ Application Status

Both servers are running:
- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:3000

---

## 🚀 Quick Start: Testing Document Upload

### Method 1: Web Interface (Recommended)

1. **Open Browser**
   - Navigate to: **http://localhost:3000/upload**
   - Or click the upload link in the main interface

2. **Select Knowledge Base**
   - Use the dropdown to choose:
     - **Auto-Map** (default) - Automatically categorizes documents
     - **Billing Knowledge Base** - For invoices, contracts, pricing
     - **Technical Knowledge Base** - For manuals, bug reports, specs
     - **Policy Knowledge Base** - For regulations, policies, compliance

3. **Upload Documents**
   - **Click to Upload:** Click the upload area and select files
   - **Drag & Drop:** Drag files onto the upload area
   - **Supported Formats:** PDF, TXT, Markdown (.md), JSON
   - **File Size Limit:** ~100 KB per file

4. **Monitor Progress**
   - Watch real-time upload progress
   - See file-by-file status updates
   - Check chunks count after successful upload

5. **Verify Success**
   - Files should show "success" status
   - Chunks count displayed (e.g., "5 chunks")
   - No error messages

---

### Method 2: API Direct (curl)

#### Upload Single File

```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@/path/to/your/document.pdf" \
  -F "target_collection=auto-map"
```

**Response:**
```json
{
  "upload_id": "uuid-here",
  "status": "queued",
  "files": [
    {
      "file_name": "document.pdf",
      "file_size": 12345,
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
  -F "files=@/path/to/document1.pdf" \
  -F "files=@/path/to/document2.txt" \
  -F "target_collection=billing_knowledge_base"
```

#### Check Upload Status

```bash
# Replace {upload_id} with ID from upload response
curl http://localhost:8000/upload/status/{upload_id}
```

---

### Method 3: Create Test Documents

#### Create Sample Files for Testing

**Billing Document:**
```bash
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

**Technical Document:**
```bash
cat > test_manual.txt << 'EOF'
Technical Manual: System XYZ
Version: 2.0
Date: 2025-01-15

Installation:
1. Unpack files
2. Run setup.sh
3. Configure database
4. Test system

Troubleshooting:
- Error 404: Check database connection
- Error 500: Verify file permissions

Specifications:
- CPU: 4 cores minimum
- RAM: 8GB minimum
- Storage: 100GB minimum
EOF
```

**Policy Document:**
```bash
cat > test_policy.txt << 'EOF'
Policy Document: Data Governance Policy
Effective Date: 2025-01-01
Policy ID: POL-2025-001

Scope:
This policy applies to all customer data handling.

Compliance Requirements:
- GDPR compliance for EU customers
- CCPA compliance for California customers
- DFARs compliance for government contracts

Data Retention:
- Customer data: 7 years
- Transaction data: 10 years
- Logs: 90 days

Security Requirements:
- Encryption at rest
- Encryption in transit
- Access controls
EOF
```

#### Upload Test Documents

1. Go to http://localhost:3000/upload
2. Select "Auto-Map" to test automatic categorization
3. Upload all three test files
4. Verify they're categorized correctly

---

## 📊 Verification Steps

### 1. Check Collections

```bash
curl http://localhost:8000/collections
```

**Expected Response:**
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

### 2. Check Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "chromadb": {
    "connected": true,
    "collections_count": 3,
    "collections": [...]
  },
  "timestamp": "2025-01-15T10:00:00"
}
```

### 3. Verify in UI

1. Upload documents via web interface
2. Wait for upload to complete
3. Verify files show "success" status
4. Check chunks count is displayed
5. Confirm target collection is shown

---

## 🧪 Testing Auto-Map Feature

The **Auto-Map** feature automatically categorizes documents based on content:

### Test Auto-Map with Different Documents

1. **Billing Document** → Should map to `billing_knowledge_base`
   - Keywords: invoice, payment, contract, pricing, billing

2. **Technical Document** → Should map to `technical_knowledge_base`
   - Keywords: installation, troubleshooting, manual, specification, bug

3. **Policy Document** → Should map to `policy_knowledge_base`
   - Keywords: policy, compliance, regulation, governance, requirement

### Steps:

1. Select "Auto-Map" in dropdown
2. Upload test documents
3. Check `target_collection` in upload status
4. Verify documents are in correct knowledge base

---

## 📝 Example Test Scenarios

### Scenario 1: Single File Upload

1. Navigate to http://localhost:3000/upload
2. Select "Billing Knowledge Base"
3. Upload `test_invoice.txt`
4. Verify:
   - ✅ Status: "success"
   - ✅ Chunks count > 0
   - ✅ Target collection: "billing_knowledge_base"

### Scenario 2: Multiple Files with Auto-Map

1. Navigate to http://localhost:3000/upload
2. Select "Auto-Map"
3. Upload all three test files
4. Verify:
   - ✅ All files processed successfully
   - ✅ Documents categorized correctly
   - ✅ Chunks created for each file

### Scenario 3: API Upload

```bash
# Create test file
echo "Test document content" > test.txt

# Upload via API
curl -X POST http://localhost:8000/upload \
  -F "files=@test.txt" \
  -F "target_collection=technical_knowledge_base"

# Check status (replace upload_id)
curl http://localhost:8000/upload/status/{upload_id}
```

---

## 🔍 Troubleshooting

### Upload Fails

1. **Check File Size**
   - Limit: ~100 KB per file
   - Verify: `ls -lh filename`

2. **Check File Format**
   - Supported: `.pdf`, `.txt`, `.md`, `.json`
   - Verify: File extension matches format

3. **Check Backend Logs**
   - Look for errors in Terminal 1 (backend)
   - Common issues:
     - ChromaDB connection errors
     - OpenAI API errors (quota, rate limits)
     - File parsing errors

### Documents Not Appearing

1. **Verify ChromaDB**
   ```bash
   curl http://localhost:8000/health
   ```
   Should show `"connected": true`

2. **Check Collections**
   ```bash
   curl http://localhost:8000/collections
   ```
   Should list all three collections

3. **Verify Upload Status**
   - Check upload status endpoint
   - Verify files show "completed" status
   - Check for error messages

---

## ✅ Success Checklist

After uploading documents, verify:

- [ ] Files show "success" status in UI
- [ ] Chunks count displayed (e.g., "5 chunks")
- [ ] Target collection shown correctly
- [ ] Collections endpoint shows 3 collections
- [ ] Health endpoint shows ChromaDB connected
- [ ] No error messages in backend logs
- [ ] No error messages in browser console

---

## 📚 Next Steps

After successful upload:

1. **Test Chat Interface**
   - Go to http://localhost:3000
   - Ask questions about uploaded documents
   - Verify agents can retrieve information

2. **Test Knowledge Base Queries**
   - Ask billing questions → Should use Billing Agent
   - Ask technical questions → Should use Technical Agent
   - Ask policy questions → Should use Policy Agent

---

## 🎯 Quick Reference

| Action | URL | Method |
|--------|-----|--------|
| Upload Page | http://localhost:3000/upload | Web UI |
| Upload API | http://localhost:8000/upload | POST |
| Check Status | http://localhost:8000/upload/status/{id} | GET |
| Collections | http://localhost:8000/collections | GET |
| Health | http://localhost:8000/health | GET |
| API Docs | http://localhost:8000/docs | Browser |

---

**Ready to test?** Start at: **http://localhost:3000/upload**

