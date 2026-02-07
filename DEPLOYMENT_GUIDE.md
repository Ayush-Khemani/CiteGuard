# CiteGuard - Complete Deployment Guide

## 📋 Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Using the Web Interface](#using-the-web-interface)
3. [Installing Chrome Extension](#installing-chrome-extension)
4. [How the System Works](#how-the-system-works)
5. [Production Deployment](#production-deployment)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.12+
- Chrome/Chromium browser
- Git (optional)

### Step 1: Start the Backend API

1. **Open Terminal** in the `backend` folder
2. **Activate Virtual Environment:**
   ```powershell
   # Windows
   .\venv\Scripts\Activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Start the Server:**
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Expected Output:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

✅ **Backend is now running!**

---

## 🌐 Using the Web Interface

1. **Open Browser** to: **http://localhost:8000**

2. **You'll see:**
   - Clean web UI with three main features
   - Plagiarism analysis tool
   - Paraphrasing suggestions
   - Citation generator

3. **Test the API:**
   - Go to **http://localhost:8000/docs** for full API documentation (Swagger UI)
   - Click "Try it out" on any endpoint to test it
   - Example: Test `/api/v1/analysis/analyze` with sample text

### Features Available

#### 📊 Plagiarism Analysis
- Paste text to check for plagiarism
- Get a percentage score (0-100%)
- See detailed analysis results
- Adjustable similarity threshold

#### ✏️ Paraphrasing
- Input text
- Get paraphrased suggestions
- Multiple style options (simple, academic, formal, casual)

#### 📚 Citation Generator
- Enter: Title, Authors, Year, Publication info
- Select citation style (APA, MLA, Chicago, Harvard, IEEE)
- Get formatted citation
- Copy to clipboard

---

## 🔧 Installing Chrome Extension

### Step 1: Prepare Extension Files
The extension files are in: `ChromeExtension/`
- `manifest.json` - Extension configuration
- `popup.html` - The popup interface
- `popup.js` - Popup functionality
- `content.js` - Web page integration
- `background.js` - Background service worker
- `content.css` - Styling

### Step 2: Load Extension in Chrome
1. **Open Chrome** and go to: `chrome://extensions`

2. **Enable Developer Mode**
   - Toggle **"Developer mode"** (top right corner)

3. **Load Unpacked Extension**
   - Click **"Load unpacked"**
   - Navigate to `ChromeExtension/` folder
   - Select it and click **"Open"**

4. **You should see:**
   - CiteGuard extension appears in the list
   - Extension icon appears in your toolbar (📋 icon)

### Step 3: Make Server Accessible to Extension
The extension needs to connect to your local API. **IMPORTANT:**
- Make sure the backend server is running (see [Local Development Setup](#local-development-setup))
- Extension connects to: `http://localhost:8000/api/v1`

---

## 💡 How the System Works

### Architecture Overview
```
┌─────────────────────────────────────────────────┐
│         User's Web Browser                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐      ┌──────────────┐        │
│  │  Web UI      │      │  Chrome Ext  │        │
│  │(HTML/CSS/JS) │      │  (Popup)     │        │
│  └──────┬───────┘      └──────┬───────┘        │
│         │                     │                │
│         └─────────┬───────────┘                │
│                   │ HTTP/JSON                  │
│                   ▼                            │
├─────────────────────────────────────────────────┤
│  FastAPI Backend (localhost:8000)              │
├─────────────────────────────────────────────────┤
│                                                 │
│  Routes:                                       │
│  ├─ /api/v1/analysis/analyze                  │
│  ├─ /api/v1/analysis/paraphrase               │
│  ├─ /api/v1/analysis/citation                 │
│  ├─ /api/v1/documents (CRUD)                  │
│  └─ /api/v1/sources (search library)          │
│                                                 │
│  Services:                                     │
│  ├─ SimilarityService (plagiarism detection)  │
│  ├─ CitationGenerator (5 styles)              │
│  └─ ParaphrasingService (AI-powered)          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Data Flow

#### 1. **Plagiarism Analysis**
```
User selects text on website
         ↓
Chrome Extension captures text
         ↓
Sends to Flask API: POST /api/v1/analysis/analyze
         ↓
API analyzes with semantic similarity
         ↓
Returns: plagiarism_score, flagged_sections
         ↓
UI displays result with color coding
```

#### 2. **Citation Generation**
```
User enters: title, authors, year, style
         ↓
Sends to API: POST /api/v1/analysis/citation
         ↓
API formats according to selected style
         ↓
Returns: formatted_citation
         ↓
User copies to clipboard
```

#### 3. **Chrome Extension Workflow**
```
User selects text on any website
         ↓
Content script detects selection
         ↓
Floating button appears: "📋 Check Plagiarism"
         ↓
User clicks button
         ↓
Background service worker sends to API
         ↓
Result notification appears on page
```

---

## 📦 Production Deployment

### Option 1: Deploy on Azure (Recommended)

#### Prerequisites
- Azure account
- Azure CLI installed
- Docker (optional, but helpful)

#### Steps
1. **Create Azure Web App**
   ```bash
   az webapp create --resource-group myResourceGroup \
     --plan myAppServicePlan --name citeguard-api
   ```

2. **Deploy Backend**
   ```bash
   # Build Docker image
   docker build -t citeguard:latest .
   
   # Push to Azure Container Registry
   az acr build --registry myRegistry --image citeguard:latest .
   
   # Deploy to Web App
   az webapp create --deployment-container-image-name citeguard:latest
   ```

3. **Publish Chrome Extension**
   - Go to [Chrome Web Store](https://chrome.google.com/webstore)
   - Register as developer ($5 one-time fee)
   - Upload extension files + screenshots
   - Submit for review

### Option 2: Deploy on Heroku
```bash
# Install Heroku CLI
heroku login
heroku create citeguard-api
git push heroku main
```

### Option 3: Deploy on DigitalOcean / Linode
1. Create VPS
2. Install Python 3.12
3. Clone repository
4. Install dependencies: `pip install -r requirements.txt`
5. Start with PM2 or systemd
6. Use Nginx as reverse proxy
7. Get SSL certificate with Let's Encrypt

### Configuration for Production
Update `backend/app/core/config.py`:
```python
# Set to False in production
DEBUG = False

# Add your domain
CORS_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]

# Use PostgreSQL instead of SQLite
DATABASE_URL = "postgresql://user:password@db-host/citeguard"

# Use Redis for caching (recommended)
REDIS_URL = "redis://redis-host:6379"
```

### Publishing Chrome Extension
1. Create Chrome Web Store developer account
2. Prepare:
   - Extension files
   - Icon (128×128px PNG)
   - Screenshots (1280×800px)
   - Description & privacy policy
3. Upload and submit for review (~1-3 hours approval)

---

## 🐛 Troubleshooting

### "Cannot connect to API" Error

**Problem:** Extension or web UI shows connection error

**Solutions:**
1. **Check backend is running:**
   ```bash
   # Test in PowerShell
   curl http://localhost:8000/api/v1/analysis/health
   ```

2. **Check port 8000 is available:**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Mac/Linux
   lsof -i :8000
   ```

3. **CORS Issue** - Add to main.py:
   ```python
   CORS_ORIGINS = ["*"]  # Allow all origins (dev only)
   ```

### "Module not found" Error

**Problem:** `ImportError: No module named 'fastapi'`

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt
```

### Extension Not Loading

**Problem:** Extension doesn't appear in `chrome://extensions`

**Solutions:**
1. Reload the page (`Ctrl+R` or `Cmd+R`)
2. Check file structure is correct
3. Verify `manifest.json` is valid JSON
4. Check Chrome console for errors (right-click popup → Inspect)

### "localhost refused to connect"

**Problem:** Getting connection refused errors

**Solutions:**
1. Make sure backend server is running
2. Check URL is exactly `http://localhost:8000` (not `https`)
3. Temporarily disable firewall for testing
4. Check if another app is using port 8000

### API Responses are Empty

**Problem:** API returns data but UI shows nothing

**Solutions:**
1. Open browser DevTools (`F12`)
2. Check Network tab for API responses
3. Check Console tab for JavaScript errors
4. Verify response format matches expected format

---

## 📊 Testing the System

### 1. Test Web Interface
```bash
# In browser
http://localhost:8000
```
- Type text in analysis box
- Click "Analyze Text"
- See score and metrics

### 2. Test API Directly
```bash
# In terminal
curl -X POST http://localhost:8000/api/v1/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a sample text for testing plagiarism detection",
    "threshold": 0.7
  }'
```

### 3. Test Chrome Extension
1. Navigate to any website
2. Select some text on the page
3. Floating button should appear
4. Click it to test plagiarism analysis
5. Check that API result appears

### 4. Test Citation Generation
```bash
curl -X POST http://localhost:8000/api/v1/analysis/citation \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Deep Learning for NLP",
    "authors": ["John Doe", "Jane Smith"],
    "year": 2024,
    "style": "apa"
  }'
```

---

## 📚 API Endpoints Reference

### Analysis Endpoints
```
POST /api/v1/analysis/analyze
- Check text for plagiarism
- Params: text, threshold
- Returns: plagiarism_score, flagged_sections, recommendations

POST /api/v1/analysis/{id}/paraphrase
- Paraphrase given text
- Params: text, style
- Returns: paraphrased_text

POST /api/v1/analysis/citation
- Generate formatted citation
- Params: title, authors, year, style
- Returns: formatted_citation

GET /api/v1/analysis/health
- Check API health
- Returns: status, version
```

### Document Management
```
GET /api/v1/documents
- List user documents

POST /api/v1/documents
- Create new document

GET /api/v1/documents/{id}
- Get document

DELETE /api/v1/documents/{id}
- Delete document
```

### Source Library
```
GET /api/v1/sources
- List sources

POST /api/v1/sources
- Add source

GET /api/v1/sources/search?query=...
- Search sources

POST /api/v1/sources/{id}/cite
- Get citation for source
```

---

## 🎯 What's Next?

### Short Term (Week 1-2)
- [ ] Test all endpoints with real data
- [ ] Set up PostgreSQL database
- [ ] Implement user authentication
- [ ] Deploy to test server

### Medium Term (Week 3-4)
- [ ] Integrate real ML models (sentence-transformers)
- [ ] Add paraphrasing API (OpenAI/Anthropic)
- [ ] User dashboard
- [ ] Document history & analytics

### Long Term (Month 2+)
- [ ] Mobile app
- [ ] Advanced plagiarism detection
- [ ] Collaboration features
- [ ] Integration with LMS platforms (Canvas, Blackboard)

---

## 📞 Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review API documentation at `/docs`
3. Check terminal output for error messages
4. Enable verbose logging: `DEBUG = True` in config

---

**Happy Plagiarism Detecting! 🎓**
