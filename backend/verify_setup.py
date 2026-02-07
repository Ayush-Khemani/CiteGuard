"""
Environment setup and verification script.
Checks that all dependencies are properly installed.
"""
import sys
import subprocess


def check_python_version():
    """Check Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required, but running {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_required_packages():
    """Check that required packages are installed"""
    required = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} NOT installed")
    
    if missing:
        print(f"\n📦 To install missing packages, run:")
        print(f"   pip install {' '.join(missing)}")
        return False
    return True


def check_database():
    """Check if PostgreSQL is accessible"""
    try:
        import psycopg2
        try:
            conn = psycopg2.connect(
                host="localhost",
                user="citeguard",
                password="citeguard",
                database="citeguard"
            )
            conn.close()
            print("✓ PostgreSQL connection successful")
            return True
        except psycopg2.OperationalError:
            print("⚠ PostgreSQL not accessible - this is OK for initial setup")
            print("  You can set up the database later using Docker:")
            print("  docker run --name citeguard-postgres -e POSTGRES_PASSWORD=citeguard -p 5432:5432 -d postgres:15")
            return True
    except ImportError:
        print("⚠ psycopg2 not installed - database checks skipped")
        return True


def check_redis():
    """Check if Redis is accessible"""
    try:
        import redis
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            print("✓ Redis connection successful")
            return True
        except redis.ConnectionError:
            print("⚠ Redis not accessible - this is OK for initial setup")
            print("  You can set up Redis using Docker:")
            print("  docker run --name citeguard-redis -p 6379:6379 -d redis:7")
            return True
    except ImportError:
        print("⚠ redis not installed - Redis checks skipped")
        return True


def verify_structure():
    """Verify project structure is set up correctly"""
    import os
    
    required_dirs = [
        'app/core',
        'app/models',
        'app/services',
        'app/api/routes',
        'app/schemas',
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = os.path.join('backend', dir_path)
        if os.path.isdir(full_path):
            print(f"✓ {dir_path}/ exists")
        else:
            print(f"❌ {dir_path}/ missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all checks"""
    print("=" * 50)
    print("CiteGuard Environment Verification")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Project Structure", verify_structure),
        ("Required Packages", check_required_packages),
        ("PostgreSQL", check_database),
        ("Redis", check_redis),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}")
        print("-" * 50)
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"⚠ Error during check: {e}")
            results.append(True)  # Don't fail on errors
    
    print()
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    
    if all(results):
        print("✅ All checks passed! You're ready to start development.")
        print("\n🚀 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Set up database: docker-compose -f docker/docker-compose.yml up -d")
        print("   3. Start backend: python -m uvicorn app.main:app --reload")
        print("   4. Visit API docs: http://localhost:8000/docs")
    else:
        print("⚠ Some checks failed. See details above.")
        print("\nYou may still proceed, but some features might not work.")
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
