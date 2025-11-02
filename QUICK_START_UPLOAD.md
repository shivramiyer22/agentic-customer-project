# Quick Start: Test Document Upload

## 🎯 Current Status

✅ **Backend:** Running on http://localhost:8000  
✅ **Frontend:** Running on http://localhost:3000  
✅ **Configuration:** All environment variables set

---

## 📤 How to Upload Documents

### Option 1: Web Interface (Easiest)

1. **Open Browser:**
   ```
   http://localhost:3000/upload
   ```

2. **Select Knowledge Base:**
   - Choose from dropdown:
     - **Auto-Map** - Auto-categorizes (recommended for testing)
     - **Billing Knowledge Base** - For invoices, contracts
     - **Technical Knowledge Base** - For manuals, specs
     - **Policy Knowledge Base** - For regulations, policies

3. **Upload Files:**
   - Click upload area OR drag & drop files
   - Supported: PDF, TXT, MD, JSON
   - Max size: ~100 KB per file

4. **Watch Progress:**
   - Real-time upload progress
   - Status updates per file
   - Chunks count after completion

---

### Option 2: API (curl)

**Upload a file:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@/path/to/document.pdf" \
  -F "target_collection=auto-map"
```

**Check status:**
```bash
# Use upload_id from response above
curl http://localhost:8000/upload/status/{upload_id}
```

---

### Option 3: Create Test Documents

**Create a test file:**
```bash
cat > test_document.txt << 'EOF'
Billing Document Test
Invoice #12345
Amount: $1,000.00
Date: 2025-01-15
Customer: Test Corp
EOF
```

**Then upload via web interface or API**

---

## ✅ Verify Upload Success

**Check collections:**
```bash
curl http://localhost:8000/collections
```

**Check health:**
```bash
curl http://localhost:8000/health
```

**In UI:**
- Files show "success" status
- Chunks count displayed
- No error messages

---

## 🔗 Quick Links

- **Upload Page:** http://localhost:3000/upload
- **Chat Interface:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

**Start testing now:** Open http://localhost:3000/upload in your browser!

