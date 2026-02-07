@echo off
REM Quick Start Guide for CiteGuard - Windows Version

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          CiteGuard - Quick Start Guide (Windows)           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📦 What Was Just Fixed:
echo   ✓ Backend folder structure organized properly
echo   ✓ All Python modules and API routes created
echo   ✓ Database migrations configured (Alembic)
echo   ✓ .env configuration template created
echo   ✓ Chrome extension files created
echo   ✓ Docker setup corrected
echo   ✓ Startup scripts provided (run.sh, run.bat)
echo.

echo 🚀 Choose How to Start:
echo.

echo OPTION 1: Docker (Recommended - Easiest)
echo   1. Make sure Docker Desktop is running
echo   2. Run: docker-compose -f docker/docker-compose.yml up -d
echo   3. Wait 30 seconds for services to start
echo   4. Visit: http://localhost:8000/docs
echo.

echo OPTION 2: Windows Direct (Click and Go)
echo   1. Navigate to: backend\run.bat
echo   2. Double-click run.bat
echo   3. A terminal will open and start the server
echo   4. When you see "Uvicorn running on http://0.0.0.0:8000"
echo   5. Open browser and visit: http://localhost:8000/docs
echo.

echo OPTION 3: Manual Setup (Full Control)
echo   cd backend
echo   python -m venv venv
echo   venv\Scripts\activate.bat
echo   pip install -r requirements.txt
echo   python -m spacy download en_core_web_sm
echo   copy ..\.env.example .env
echo   REM Start PostgreSQL and Redis
echo   uvicorn app.main:app --reload
echo.

echo 📚 Documentation Files:
echo   - README.md ................. Complete documentation
echo   - GettingStarted.md ......... Original setup guide
echo   - FIX_SUMMARY.md ............ What was fixed
echo   - Roadmap.md ................ Development plan
echo.

echo ⚙️  Quick Configuration:
echo   1. Open backend folder
echo   2. Copy: .env.example to .env
echo   3. Edit .env file:
echo      - DEBUG=True (for development)
echo      - DATABASE_URL (set to your PostgreSQL)
echo      - REDIS_URL (set to your Redis)
echo   4. Save and close
echo.

echo 🔍 Verify Setup (Optional):
echo   cd backend
echo   python verify_setup.py
echo.

echo 📝 Testing the API:
echo   Once backend is running:
echo   1. Visit: http://localhost:8000/docs
echo   2. You'll see Swagger UI (interactive API docs)
echo   3. Click "Try it out" on any endpoint
echo   4. Fill in parameters and click "Execute"
echo.

echo 🐳 Docker Useful Commands:
echo   docker-compose -f docker/docker-compose.yml up -d      (Start)
echo   docker-compose -f docker/docker-compose.yml down        (Stop)
echo   docker-compose -f docker/docker-compose.yml logs -f     (View logs)
echo   docker ps                                               (See running containers)
echo.

echo 🧪 Database Credentials (if using Docker):
echo   Host: localhost
echo   Port: 5432
echo   User: citeguard
echo   Password: citeguard
echo   Database: citeguard
echo.

echo 💾 Cache Credentials (if using Docker):
echo   Host: localhost
echo   Port: 6379
echo.

echo 📋 What Each File Does:
echo   backend/run.bat ........... Starts the API server
echo   backend/verify_setup.py ... Checks your setup
echo   .env.example .............. Configuration template
echo   docker-compose.yml ........ Docker services config
echo.

echo 🔗 Important URLs:
echo   API Docs: http://localhost:8000/docs
echo   Health Check: http://localhost:8000/health
echo   API Root: http://localhost:8000/
echo.

echo 💡 Tips:
echo   - Use Docker for easiest setup (no dependencies to install)
echo   - Swagger UI at /docs is your best friend
echo   - Check .env.example for all configuration options
echo   - Run verify_setup.py if something isn't working
echo.

echo ═══════════════════════════════════════════════════════════
echo ✨ You're all set! Choose an option above to get started.
echo ═══════════════════════════════════════════════════════════
echo.

pause
