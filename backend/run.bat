@echo off
REM Backend startup script for Windows
REM This script sets up and runs the FastAPI backend

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ========================================
echo   CiteGuard Backend - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment
        echo Make sure Python 3.11+ is installed and in PATH
        echo.
        pause
        exit /b 1
    )
)

REM Install dependencies directly using venv python
echo.
echo Installing dependencies...
echo (This may take a few minutes the first time...)
echo.

"venv\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install
    echo But we'll try to start the server anyway...
    echo.
)

REM Create .env from template if it doesn't exist
if not exist ".env" (
    if exist "..\..env.example" (
        echo Creating .env from template...
        copy ..\..env.example .env >nul
    )
)

echo.
echo ========================================
echo   Starting FastAPI Server
echo ========================================
echo.
echo API will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server using venv python
"venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

REM If we get here, server stopped
pause
