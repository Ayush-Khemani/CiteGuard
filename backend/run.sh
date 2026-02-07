#!/bin/bash
# Backend startup script for Unix/Linux/macOS

set -e

cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "  CiteGuard Backend - Starting..."
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "(This may take a few minutes the first time...)"
echo ""
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some dependencies failed to install"
    echo "But we'll try to start the server anyway..."
    echo ""
fi

# Copy .env file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f "../.env.example" ]; then
        echo "Creating .env from template..."
        cp ../.env.example .env
    fi
fi

echo ""
echo "========================================"
echo "  Starting FastAPI Server"
echo "========================================"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
