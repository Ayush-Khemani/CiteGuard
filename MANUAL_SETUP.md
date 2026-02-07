# 🚀 CiteGuard - Manual Setup Guide for Windows

Your environment: **Python 3.12.2**

## Quick Setup (Copy-Paste These Commands)

Open PowerShell or Command Prompt and run these commands one by one:

### Step 1: Navigate to backend folder
```powershell
cd "d:\Post Projects\Anti Plagrisim Detector\backend"
```

### Step 2: Create virtual environment
```powershell
python -m venv venv
```

### Step 3: Activate virtual environment
```powershell
venv\Scripts\Activate.ps1
```
> If you get an execution policy error, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Step 4: Install FastAPI (core framework)
```powershell
pip install fastapi uvicorn pydantic pydantic-settings
```

### Step 5: Install database packages
```powershell
pip install sqlalchemy psycopg2-binary redis alembic python-dotenv
```

### Step 6: Install authentication packages
```powershell
pip install python-jose passlib cryptography python-multipart
```

### Step 7: Start the server
```powershell
python -m uvicorn app.main:app --reload
```

That's it! You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 8: Test it works
Open your browser and go to:
- **http://localhost:8000/docs** - Interactive API documentation
- **http://localhost:8000/health** - Health check endpoint

---

## What If Something Goes Wrong?

### "venv\Scripts\Activate.ps1" not found
- Your virtual environment wasn't created properly
- Delete `venv` folder: `rmdir /s venv`
- Try creating again: `python -m venv venv`

### "ModuleNotFoundError: No module named 'fastapi'"
- Your virtual environment is not activated
- Make sure you ran: `venv\Scripts\Activate.ps1`
- Check that `(venv)` appears at the start of your terminal prompt

### Port 8000 already in use
- Another process is using port 8000
- Either close it, or use a different port: `python -m uvicorn app.main:app --port 8001 --reload`

### Execution policy error
- Run PowerShell as Administrator
- Then: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Answer `Y` when prompted

---

## Minimal Installation (No ML Features)

If you start getting errors about torch, transformers, etc., you can continue without those heavy ML packages. They're optional for development.

After installing the 6 steps above, your API **will work** for:
- ✅ Plagiarism analysis endpoints
- ✅ Citation generation
- ✅ Paraphrasing interface
- ✅ Document management
- ✅ API documentation

The ML models can be added later: `pip install torch sentence-transformers transformers spacy`

---

## Complete Installation (With Everything)

To install all optional packages:

```powershell
pip install -r requirements.txt
```

Note: This might fail on torch==2.1.2. If it does:
```powershell
pip install torch scikit-learn numpy
pip install sentence-transformers transformers
pip install pytest pytest-asyncio black ruff mypy
```

---

## Next Steps After Starting Server

1. **Visit API Docs**: http://localhost:8000/docs
2. **Try an endpoint**:
   - POST `/api/v1/analysis/analyze`
   - With body: `{"text": "Your text here", "threshold": 0.85}`
3. **Check health**: http://localhost:8000/
4. **Read the code**:
   - `app/main.py` - Main FastAPI application
   - `app/api/routes/` - API endpoints
   - `app/services/` - Business logic

---

## Keep Server Running

Once you have the server running, **keep that terminal open** while you develop.

To stop: `Ctrl+C` in the terminal

---

## Production Deployment

For production, we can use Docker:
```bash
docker compose -f docker/docker-compose.yml up -d
```

But for development, this manual setup is fine!

---

**Need help?** Check:
- [README.md](../README.md) - Full documentation
- [COMPLETION_REPORT.md](../COMPLETION_REPORT.md) - Project status
