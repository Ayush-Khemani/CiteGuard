# CiteGuard - Academic Plagiarism Prevention System

A comprehensive plagiarism detection and academic integrity tool with real-time analysis, smart citations, and AI-powered paraphrasing.

## 🎯 Features

- **Real-time Plagiarism Detection**: Analyze text as you write with semantic similarity detection
- **Smart Citation Generation**: Generate properly formatted citations (APA, MLA, Chicago, Harvard, IEEE)
- **AI-Powered Paraphrasing**: Get multiple paraphrasing suggestions to rephrase content
- **Chrome Extension**: Works seamlessly with Google Docs, Microsoft Office, Notion, and Overleaf
- **Academic Database Integration**: Search and cite sources from Semantic Scholar and CrossRef

## 📋 Requirements

### Prerequisites
- **Python 3.11+** - For backend development
- **Node.js 18+** - For extension development (optional)
- **PostgreSQL 15+** - Database
- **Redis 7+** - Caching layer

### Optional
- **Docker & Docker Compose** - For containerized setup (recommended)
- **OpenAI API Key** - For GPT-based paraphrasing
- **Anthropic API Key** - For Claude-based paraphrasing

## 🚀 Quick Start (5 minutes)

### Option 1: Local Python Setup (Windows/Mac/Linux)

1. **Navigate to backend folder**:
   ```bash
   cd backend
   ```

2. **Run startup script**:
   - **Windows**: Double-click `run.bat`
   - **Mac/Linux**: `bash run.sh`

   This will:
   - Create a Python virtual environment
   - Install all dependencies
   - Download NLP models
   - Start the API on `http://localhost:8000`

3. **Verify installation**:
   - Visit `http://localhost:8000/docs` - You should see the interactive API documentation

### Option 2: Docker Setup (Recommended)

1. **Install Docker** from https://www.docker.com/products/docker-desktop

2. **Start services** from the project root:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

3. **Verify services**:
   ```bash
   docker ps
   ```
   You should see `citeguard-postgres`, `citeguard-redis`, and `citeguard-backend` containers

4. **Access API**:
   - API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

## ⚙️ Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your settings:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://citeguard:citeguard@localhost:5432/citeguard
   REDIS_URL=redis://localhost:6379/0
   
   # Optional - for LLM features
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Start database services** (if not using Docker):

   **PostgreSQL**:
   - Ubuntu/Debian: `sudo service postgresql start`
   - macOS: `brew services start postgresql`
   - Windows: Use PostgreSQL installer or WSL

   **Redis**:
   - Ubuntu/Debian: `sudo service redis-server start`
   - macOS: `brew services start redis`
   - Windows: Use WSL or Windows Redis port

## 📚 Project Structure

```
.
├── backend/                        # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/            # API endpoints (analysis, auth, documents, sources)
│   │   ├── services/              # Business logic (similarity, citation, paraphrasing)
│   │   ├── models/                # SQLAlchemy database models
│   │   ├── schemas/               # Pydantic request/response schemas
│   │   ├── core/                  # Configuration, security, database
│   │   └── main.py               # FastAPI application
│   ├── alembic/                   # Database migrations
│   ├── requirements.txt           # Python dependencies
│   ├── run.sh & run.bat          # Startup scripts
│   └── .env                       # Environment variables (create from .env.example)
│
├── extension/                     # Chrome extension
│   ├── manifest.json             # Extension configuration
│   ├── background.js             # Service worker
│   ├── content.js & content.css  # Page injection script
│   ├── popup.html & popup.js     # Extension popup UI
│   └── package.json              # Extension dependencies
│
├── docker/                        # Docker configuration
│   ├── docker-compose.yml        # Multi-container setup
│   └── Dockerfile.backend        # Backend container image
│
├── ml/                            # Machine learning models
│   ├── similarity/               # Plagiarism detection models
│   └── paraphrasing/             # Paraphrasing models
│
├── .env.example                   # Environment template
├── GettingStarted.md             # Setup guide
└── Roadmap.md                    # Development roadmap
```

## 🔌 API Endpoints

### Health Check
- `GET /health` - API health status
- `GET /` - Root endpoint with API info

### Analysis (Core Feature)
- `POST /api/v1/analysis/analyze` - Analyze text for plagiarism
- `POST /api/v1/analysis/citation` - Generate citations
- `POST /api/v1/analysis/paraphrase` - Get paraphrasing suggestions

### Authentication (Coming Soon)
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user

### Documents
- `GET /api/v1/documents/` - List user documents
- `POST /api/v1/documents/` - Create document
- `GET /api/v1/documents/{id}` - Get document
- `PUT /api/v1/documents/{id}` - Update document
- `DELETE /api/v1/documents/{id}` - Delete document

### Sources
- `GET /api/v1/sources/` - List user sources
- `POST /api/v1/sources/` - Add source to library
- `DELETE /api/v1/sources/{id}` - Remove source

## 🧪 Testing the API

### Using Swagger UI (Interactive)
1. Start the backend
2. Navigate to `http://localhost:8000/docs`
3. Click "Try it out" on any endpoint

### Using cURL
```bash
# Analyze text
curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text":"Your text here","threshold":0.85}'

# Generate citation
curl -X POST "http://localhost:8000/api/v1/analysis/citation" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Paper Title",
    "authors":["Author Name"],
    "year":2024,
    "source_type":"article",
    "citation_style":"APA"
  }'
```

### Using Postman
1. Import the API endpoints into Postman
2. Set `http://localhost:8000` as base URL
3. Test each endpoint with sample data

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U citeguard -d citeguard -c "SELECT 1"

# Check Redis is running
redis-cli ping
```

### Dependencies Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Virtual Environment Issues
```bash
# Delete and recreate venv
rm -rf venv  # rmdir /s venv on Windows
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
```

## 📦 Development

### Install Dev Dependencies
```bash
pip install -r requirements-dev.txt  # When available
```

### Run Tests
```bash
pytest backend/
```

### Code Formatting
```bash
black backend/
flake8 backend/
```

### View Logs
```bash
# Docker logs
docker-compose -f docker/docker-compose.yml logs -f backend

# Local logs
tail -f logs/app.log
```

## 🚢 Deployment

### To Azure
```bash
az login
az containerapp up --source . --name citeguard-api --resource-group citeguard-rg
```

### Using Docker
```bash
docker build -f docker/Dockerfile.backend -t citeguard-api .
docker run -p 8000:8000 --env-file .env citeguard-api
```

## 📖 Documentation

- [Getting Started Guide](./GettingStarted.md)
- [Development Roadmap](./Roadmap.md)
- [API Documentation](http://localhost:8000/docs) - Available after starting backend

## 🤝 Contributing

1. Create a branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## 📄 License

CiteGuard is open source software. License details coming soon.

## ✅ Current Status

**Phase 1: MVP (In Progress)**
- ✅ Backend API structure
- ✅ Core services (similarity, citation, paraphrasing)
- ✅ Extension scaffolding
- ⏳ Database integration (next)
- ⏳ Authentication (next)
- ⏳ Extension UI (next)

See [Roadmap.md](./Roadmap.md) for detailed development plan.

## 📞 Support

- 📧 Email: support@citeguard.com (coming soon)
- 💬 GitHub Issues: Report bugs and request features
- 📚 Documentation: See GettingStarted.md

---

**Started**: February 2026  
**Current Version**: 0.1.0 (Beta)
