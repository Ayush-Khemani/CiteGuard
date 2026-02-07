"""
Vercel serverless function handler for FastAPI app.
This file is the entry point for Vercel's Python serverless runtime.
"""
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = str(Path(__file__).parent.parent / "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Set environment mode
os.environ.setdefault("DEBUG", "False")

# Import and export the FastAPI app
from app.main import app

# Vercel expects an ASGI app named 'app'
__all__ = ["app"]
