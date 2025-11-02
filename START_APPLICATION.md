# How to Start the Application and Test Document Upload

## ✅ Current Status

Both servers are **running**:
- ✅ **Backend API:** http://localhost:8000
- ✅ **Frontend:** http://localhost:3000
- ✅ **Environment:** Configured

---

## 🚀 Start Instructions (If Servers Are Not Running)

### Start Backend Server

**Terminal 1:**
```bash
cd /Users/manasaiyer/Desktop/SKI\ -\ ASU/Vibe-Coding/agentic-customer-project/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

### Start Frontend Server

**Terminal 2 (New Terminal):**
```bash
cd /Users/manasaiyer/Desktop/SKI\ -\ ASU/Vibe-Coding/agentic-customer-project/frontend
npm run dev
```

**Expected Output:**
```
▲ Next.js 16.0.1
- Local:        http://localhost:3000
```

---

## 📤 Test Document Upload

### Quick Test: Web Interface

1. **Open Browser:**
   ```
   http://localhost:3000/upload
   ```

2. **Select Knowledge Base:**
   - Choose **"Auto-Map"** from dropdown (default)

3. **Upload Test Document:**
   
   **Option A: Create a test file**
   ```bash
   cd ~/Desktop/SKI\ -\ ASU/Vibe-Coding/agentic-customer-project
   cat > test_document.txt << 'EOF'
   Invoice #12345
   Customer: Test Corp
   Amount: $1,000.00
   Date: 2025-01-15
   EOF
   ```
   
   Then:
   - Go to http://localhost:3000/upload
   - Click upload area
   - Select `test_document.txt`
   - Watch upload progress
   - Verify "success" status and chunks count

   **Option B: Use existing file**
   - Select any PDF, TXT, MD, or JSON file
   - Upload via web interface

4. **Verify Success:**
   - ✅ File shows "success" status
   - ✅ Chunks count displayed (e.g., "5 chunks")
   - ✅ Target collection shown
   - ✅ No error messages

---

### Test via API (curl)

**Upload a file:**
```bash
# Create test file first
echo "Test document content" > test.txt

# Upload via API
curl -X POST http://localhost:8000/upload \
  -F "files=@test.txt" \
  -F "target_collection=auto-map"
```

**Check upload status:**
```bash
# Use upload_id from response above
curl http://localhost:8000/upload/status/{upload_id}
```

**Check collections:**
```bash
curl http://localhost:8000/collections
```

---

## ✅ Verification

### 1. Check Health
```bash
curl http://localhost:8000/health
```
Should show: `"status": "healthy"` and `"connected": true` for ChromaDB

### 2. Check Collections
```bash
curl http://localhost:8000/collections
```
Should list all 3 collections:
- `billing_knowledge_base`
- `technical_knowledge_base`
- `policy_knowledge_base`

### 3. Verify in UI
- Go to http://localhost:3000/upload
- Upload a test file
- Verify success status and chunks count

---

## 🎯 Quick Links

| Service | URL | Purpose |
|---------|-----|---------|
| **Upload Page** | http://localhost:3000/upload | Upload documents |
| **Chat Interface** | http://localhost:3000 | Main chat UI |
| **API Docs** | http://localhost:8000/docs | API documentation |
| **Health Check** | http://localhost:8000/health | System status |
| **Collections** | http://localhost:8000/collections | List knowledge bases |

---

## 📋 Test Checklist

After starting servers:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can access http://localhost:3000/upload
- [ ] Can select knowledge base from dropdown
- [ ] Can upload files (click or drag-drop)
- [ ] Upload progress updates correctly
- [ ] Files show "success" status
- [ ] Chunks count displayed
- [ ] Collections endpoint returns 3 collections
- [ ] Health endpoint shows ChromaDB connected

---

## 🔧 Troubleshooting

**Backend won't start?**
- Check Python version: `python3 --version` (should be 3.11+)
- Activate virtual environment: `source venv/bin/activate`
- Check .env file exists in `backend/` directory
- Verify OpenAI API key is set

**Frontend won't start?**
- Check Node.js version: `node --version` (should be 18+)
- Install dependencies: `npm install`
- Check .env.local file exists in `frontend/` directory

**Upload fails?**
- Check file size (≤ 100 KB)
- Check file format (PDF, TXT, MD, JSON)
- Check backend logs in Terminal 1
- Verify ChromaDB connection

---

## 🚀 Ready to Test?

**Start at:** **http://localhost:3000/upload**

1. Select "Auto-Map"
2. Upload a test document
3. Watch it get categorized
4. Verify success!

