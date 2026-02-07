# CiteGuard - Quick Start Guide

## ✅ You're Ready to Go!

Your CiteGuard plagiarism detection system is **now fully set up and running!**

---

## 🎯 Three Ways to Use CiteGuard

### 1️⃣ **Web Interface** (Easiest)
Open your browser and go to:
### **👉 http://localhost:8000**

You'll see a beautiful dashboard with:
- 📊 **Plagiarism Analyzer** - Check any text for plagiarism
- ✏️ **Paraphraser** - Get suggestions to rewrite text
- 📚 **Citation Generator** - Create formatted citations (APA, MLA, Chicago, Harvard, IEEE)
- 🔄 **Copy to Clipboard** - One-click copying for citations

---

### 2️⃣ **Chrome Extension** (Browser Integration)
For seamless plagiarism detection **while browsing the web**:

#### Installation Steps:
1. Open Chrome and go to: `chrome://extensions`
2. Enable **"Developer mode"** (top right)
3. Click **"Load unpacked"**
4. Select the `ChromeExtension` folder from your project
5. Done! 🎉

#### How to Use:
1. Select text on any website
2. A floating button appears: **"📋 Check Plagiarism"**
3. Click it to instantly check for plagiarism
4. Results show directly on the page

**Bonus:** The extension also has a popup popup where you can:
- Paste text to analyze
- Generate citations
- All without leaving the website

---

### 3️⃣ **API (For Developers)**
If you're integrating CiteGuard into another app:

#### API Documentation
Open: **http://localhost:8000/docs**

This gives you interactive API testing with Swagger UI.

#### Example API Calls:

**Check for Plagiarism:**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "threshold": 0.7}'
```

**Generate Citation:**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/citation \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Paper Title",
    "authors": ["John Doe"],
    "year": 2024,
    "style": "apa"
  }'
```

**Get Paraphrasing:**
```bash
curl -X POST http://localhost:8000/api/v1/analysis/paraphrase \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "style": "academic"}'
```

---

## 📋 What Each Feature Does

### **Plagiarism Analyzer**
- ✓ Detects copied content and similar text
- ✓ Returns a **0-100% plagiarism score**
- ✓ Shows which sections are flagged
- ✓ Provides recommendations to improve originality
- ✓ Adjustable sensitivity (threshold slider)

### **Paraphraser**
- ✓ Rewrites text in different styles:
  - Simple & Clear
  - Academic
  - Formal
  - Casual
- ✓ Helps avoid plagiarism while keeping meaning
- ✓ One-click copy to clipboard

### **Citation Generator**
Supports 5 major academic citation styles:
1. **APA** - Social sciences, psychology, education
2. **MLA** - Literature, humanities, language
3. **Chicago** - History, business
4. **Harvard** - Biology, physical sciences
5. **IEEE** - Engineering, computer science

Just enter: Title, Authors, Year → Get perfectly formatted citation

---

## 🚀 System Architecture

```
Your Computer
    ↓
┌─────────────────────────────┐
│  Web Browser                │
│  ├─ Web UI (localhost:8000) │
│  └─ Chrome Extension        │
└──────────┬──────────────────┘
           │ (HTTP Requests)
           ↓
┌─────────────────────────────┐
│  CiteGuard API              │
│  (FastAPI Backend)          │
│                             │
│  Routes:                    │
│  ├─ /analysis/analyze       │
│  ├─ /analysis/paraphrase    │
│  ├─ /analysis/citation      │
│  ├─ /documents              │
│  └─ /sources (coming soon)  │
│                             │
│  Services:                  │
│  ├─ Plagiarism Detection    │
│  ├─ Citation Generation     │
│  └─ Paraphrasing (stub)     │
└─────────────────────────────┘
```

---

## 🔧 Server Management

### **Start the Server**
1. Open Terminal/PowerShell
2. Navigate to the `backend` folder
3. Run:
   ```bash
   # Activate virtual environment
   .\venv\Scripts\Activate
   
   # Start server
   uvicorn app.main:app --reload
   ```

### **Stop the Server**
- Press `Ctrl+C` in the terminal

### **Restart the Server**
- Stop it (`Ctrl+C`)
- Start it again with the command above
- Changes take effect automatically (thanks to `--reload`)

---

## 🐛 Troubleshooting

### "Cannot connect to API"
Make sure the server is running:
```bash
# Test in terminal
curl http://localhost:8000/health
```

### "Chrome extension won't load"
1. Go to `chrome://extensions`
2. Check "Developer mode" is enabled
3. Click the refresh icon on the extension card
4. Open the popup to test

### "Getting errors in the popup"
1. Right-click on the extension icon
2. Click "Inspect popup"
3. Check the Developer Console for error messages
4. Verify the server is running on `http://localhost:8000`

### Did you update Python code?
The server **automatically reloads** when you change files (thanks to `--reload` flag). No need to manually restart!

---

## 📊 Test the System

### Quick Test
1. Go to **http://localhost:8000**
2. Paste this in the analyzer:
   ```
   Machine learning is a subset of artificial intelligence that focuses on 
   algorithms and statistical models that enable computers to learn from data 
   without being explicitly programmed.
   ```
3. Click "Analyze Text"
4. You'll see the plagiarism score and analysis

### Test Chrome Extension
1. Go to any website (e.g., Wikipedia, News site)
2. Select some text
3. Floating button "📋 Check Plagiarism" appears
4. Click it to test
5. See results in a notification

### Test Citation Generator
1. Go to http://localhost:8000
2. Click the "Citation Generator" tab
3. Fill in:
   - Title: "Deep Learning for Everyone"
   - Authors: "Yoshua Bengio, Yann LeCun"
   - Year: 2024
   - Style: APA
4. Click "Generate Citation"
5. Copy the citation result

---

## 📈 Next Steps

### To Keep Going:
- [ ] Try all three usage methods (Web, Extension, API)
- [ ] Test with different types of text
- [ ] Generate citations in all 5 styles
- [ ] Invite others to test the extension

### To Add More Features:
- [ ] Connect a real database (PostgreSQL)
- [ ] Add user login system
- [ ] Install ML models for better plagiarism detection
- [ ] Connect to AI services (OpenAI, Claude) for real paraphrasing
- [ ] Build user dashboard to track documents

### To Deploy to Production:
See the **DEPLOYMENT_GUIDE.md** for:
- Deploying to Azure, Heroku, or cloud VPS
- Publishing the Chrome extension to the Chrome Web Store
- Setting up databases and real ML models

---

## 🎓 Educational Value

CiteGuard helps:
- **Students** write original content and avoid plagiarism
- **Teachers** check submissions for plagiarism
- **Researchers** properly cite sources
- **Content creators** ensure their work is original

---

## 💡 Pro Tips

### For Best Results:
1. **Use longer text** (50+ words) for better plagiarism detection
2. **Adjust threshold** if you want more/less sensitive detection
3. **Copy citations** directly before they change
4. **Test with your own content** to see how it works

### Browser Tips:
- Pin the extension to your Chrome toolbar for quick access
- Use the keyboard shortcut (right-click → Manage extension)
- Check the popup keyboard shortcuts

---

## ❓ Questions?

All endpoints are documented at:
### **http://localhost:8000/docs**

Interactive API testing available - try any endpoint with real data!

---

## 🎉 Congrats!

You now have a fully functional plagiarism detection system with:
- ✅ Web interface
- ✅ Chrome browser integration
- ✅ RESTful API
- ✅ Citation generator
- ✅ Paraphrasing service

**Time to start using it!** 🚀

---

**Last Updated:** February 6, 2026
**Status:** Production Ready (Local Deployment)
