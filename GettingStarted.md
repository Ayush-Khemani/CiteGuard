# Getting Started with CiteGuard Development

This guide will help you set up the development environment and start building CiteGuard.

## Prerequisites

### Required
- **Python 3.11+**: For backend development
- **Node.js 18+**: For extension development
- **Docker & Docker Compose**: For local services (PostgreSQL, Redis)
- **Git**: Version control

### Recommended
- **VS Code** with extensions:
  - Python
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
- **Postman** or **Insomnia**: For API testing

## Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Navigate to project directory
cd plagiarism-prevention

# Set up Python virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 2. Environment Configuration

Create `.env` file in `backend/` directory:

```bash
# backend/.env
DEBUG=True
SECRET_KEY=your-super-secret-key-change-this

# Database (use Docker or local PostgreSQL)
DATABASE_URL=postgresql://citeguard:citeguard@localhost:5432/citeguard

# Redis (use Docker or local Redis)
REDIS_URL=redis://localhost:6379/0

# AI APIs (optional for MVP - we use local models)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# External APIs (optional)
SEMANTIC_SCHOLAR_API_KEY=
CROSSREF_EMAIL=your-email@example.com
```

### 3. Start Backend Services

**Option A: Using Docker (Recommended)**

```bash
# From project root
cd docker
docker-compose up -d postgres redis

# Wait for services to be healthy
docker-compose ps
```

**Option B: Local PostgreSQL and Redis**

```bash
# Install and start PostgreSQL
sudo apt-get install postgresql  # Ubuntu/Debian
brew install postgresql  # macOS

# Install and start Redis
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis  # macOS

# Start services
sudo service postgresql start
sudo service redis-server start
```

### 4. Initialize Database

```bash
cd backend

# Create database tables
# TODO: Add Alembic migration commands
# For now, tables will be created on first run
```

### 5. Run Backend API

```bash
cd backend
source venv/bin/activate

# Run development server
python -m uvicorn app.main:app --reload --port 8000

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 6. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Analyze text (minimal example)
curl -X POST http://localhost:8000/api/v1/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Climate change is causing significant alterations to global weather patterns.",
    "sources": []
  }'
```

## Development Workflow

### Backend Development

```bash
# Activate virtual environment
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# Run tests (when implemented)
pytest

# Check code quality
black app/
ruff check app/
mypy app/
```

### Extension Development

```bash
cd extension

# Install dependencies
npm install

# Development build (with watch mode)
npm run dev

# Load extension in Chrome:
# 1. Go to chrome://extensions/
# 2. Enable "Developer mode"
# 3. Click "Load unpacked"
# 4. Select the extension/dist folder
```

## Project Structure Overview

```
citeguard/
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   └── routes/
│   │   │       ├── analysis.py    # Core analysis endpoints ⭐
│   │   │       ├── auth.py        # Authentication
│   │   │       ├── documents.py   # Document management
│   │   │       └── sources.py     # Source management
│   │   ├── services/         # Business logic
│   │   │   ├── similarity.py      # Similarity detection ⭐
│   │   │   ├── citation.py        # Citation generation ⭐
│   │   │   └── paraphrasing.py    # AI paraphrasing ⭐
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── core/             # Configuration
│   └── requirements.txt
├── extension/                 # Chrome extension
│   ├── src/
│   │   ├── background/       # Service worker
│   │   ├── content/          # Content scripts
│   │   ├── popup/            # Extension popup
│   │   └── sidebar/          # Analysis sidebar
│   ├── manifest.json
│   └── package.json
├── docker/                    # Docker configs
│   ├── docker-compose.yml
│   └── Dockerfile.backend
└── README.md
```

## Key Features to Implement (Priority Order)

### Week 1: Core Backend
- [x] Similarity detection service
- [x] Citation generation service
- [x] Paraphrasing service
- [x] Analysis API endpoints
- [ ] Database integration
- [ ] User authentication

### Week 2: Extension Basics
- [ ] Content script injection
- [ ] Text selection detection
- [ ] Communication with backend
- [ ] Basic UI overlay

### Week 3: Integration
- [ ] Real-time analysis
- [ ] Citation suggestion UI
- [ ] Paraphrasing UI
- [ ] Source management

### Week 4: Polish
- [ ] Error handling
- [ ] Performance optimization
- [ ] User testing
- [ ] Bug fixes

## Testing Locally

### Test Similarity Detection

```python
# backend/test_similarity.py
from app.services.similarity import get_similarity_service

service = get_similarity_service()

document = """
Climate change is causing significant alterations to global 
weather patterns, leading to more frequent extreme weather events.
"""

sources = [
    {
        "id": 1,
        "title": "Climate Report 2024",
        "text": """
        Global warming is resulting in major changes to weather patterns
        worldwide, causing an increase in extreme weather occurrences.
        """
    }
]

result = service.analyze_document(document, sources)
print(f"Health Score: {result['overall_score']}")
print(f"Matches: {result['total_matches']}")
```

### Test Citation Generation

```python
# backend/test_citation.py
from app.services.citation import CitationGenerator, SourceMetadata

generator = CitationGenerator()

metadata = SourceMetadata(
    title="The Impact of AI on Academic Writing",
    authors=["John Smith", "Jane Doe"],
    year=2024,
    publication_name="Journal of Education",
    source_type="article"
)

citation = generator.generate_citation(metadata)
print(citation["full"])
print(citation["in_text"])
```

## Common Issues & Solutions

### Issue: Model download fails
```bash
# Solution: Download manually
python -m spacy download en_core_web_sm

# Or download smaller model
python -m spacy download en_core_web_md
```

### Issue: Port 8000 already in use
```bash
# Solution: Kill process or use different port
lsof -ti:8000 | xargs kill -9  # Kill process
uvicorn app.main:app --reload --port 8001  # Use different port
```

### Issue: Database connection fails
```bash
# Solution: Check Docker containers
docker-compose ps
docker-compose logs postgres

# Or check local PostgreSQL
sudo service postgresql status
```

### Issue: Out of memory when loading models
```bash
# Solution: Use smaller model
# In app/core/config.py, change:
SIMILARITY_MODEL = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # Smaller
```

## Next Steps

1. **Read the Architecture Docs**: Understand how components interact
2. **Explore the API**: Try all endpoints in `/docs`
3. **Build the Extension**: Start with content script
4. **Join Development**: Pick an issue and start coding!

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Sentence Transformers**: https://www.sbert.net/
- **Chrome Extension Dev**: https://developer.chrome.com/docs/extensions/
- **React Docs**: https://react.dev/

## Getting Help

- **Issues**: Check GitHub issues or create new one
- **Discord**: Join our development server (link in README)
- **Email**: ayush.kumar.elte@gmail.com

---

Happy coding! 🚀