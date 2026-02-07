#!/usr/bin/env python
"""
CiteGuard Backend Startup Script
Installs dependencies and starts the API server
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command"""
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}\n")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    """Main startup routine"""
    print("\n" + "="*50)
    print("  CiteGuard Backend Startup")
    print("="*50 + "\n")
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Step 1: Upgrade pip
    print("\n1️⃣  Upgrading pip...")
    run_command(
        f"{sys.executable} -m pip install --upgrade pip setuptools",
        "Upgrading pip and setuptools"
    )
    
    # Step 2: Install core dependencies
    print("\n2️⃣  Installing core dependencies...")
    core_packages = [
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "pydantic==2.5.3",
        "pydantic-settings==2.1.0",
        "sqlalchemy==2.0.25",
        "redis==5.0.1",
        "python-dotenv==1.0.0",
    ]
    
    run_command(
        f"{sys.executable} -m pip install {' '.join(core_packages)}",
        "Installing Core Dependencies (FastAPI, Database, etc.)"
    )
    
    # Step 3: Install optional dependencies
    print("\n3️⃣  Installing optional dependencies...")
    optional_packages = [
        "alembic==1.13.1",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "httpx==0.26.0",
    ]
    
    run_command(
        f"{sys.executable} -m pip install {' '.join(optional_packages)}",
        "Installing Optional Dependencies"
    )
    
    # Step 4: Create .env if doesn't exist
    print("\n4️⃣  Checking configuration...")
    env_file = backend_dir / ".env"
    env_example = backend_dir.parent / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print(f"Creating .env from template...")
        with open(env_example) as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✓ .env created")
    elif env_file.exists():
        print("✓ .env already exists")
    else:
        print("⚠ .env.example not found, skipping")
    
    # Step 5: Start server
    print("\n5️⃣  Starting FastAPI server...")
    print(f"\n{'='*50}")
    print("  🚀 FastAPI Server Starting")
    print(f"{'='*50}")
    print(f"\n📍 API URL:  http://localhost:8000")
    print(f"📖 Docs:     http://localhost:8000/docs")
    print(f"\nPress Ctrl+C to stop\n")
    
    run_command(
        f"{sys.executable} -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload",
        "Running FastAPI Server"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
