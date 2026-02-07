#!/usr/bin/env bash
# Quick Start Guide for CiteGuard

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          CiteGuard - Quick Start Guide                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}📦 What Was Just Fixed:${NC}"
echo "  ✓ Backend folder structure organized properly"
echo "  ✓ All Python modules and API routes created"
echo "  ✓ Database migrations configured (Alembic)"
echo "  ✓ .env configuration template created"
echo "  ✓ Chrome extension files created"
echo "  ✓ Docker setup corrected"
echo "  ✓ Startup scripts provided (run.sh, run.bat)"
echo ""

echo -e "${YELLOW}🚀 Choose How to Start:${NC}"
echo ""

echo -e "${GREEN}Option 1: Docker (Easiest - Recommended)${NC}"
echo "  docker-compose -f docker/docker-compose.yml up -d"
echo "  # Wait 30 seconds for services to start"
echo "  # Then visit: http://localhost:8000/docs"
echo ""

echo -e "${GREEN}Option 2: Windows (Double-click)${NC}"
echo "  1. Navigate to: backend\\run.bat"
echo "  2. Double-click run.bat"
echo "  3. Wait for server to start (gives you a terminal)"
echo "  4. Visit: http://localhost:8000/docs"
echo ""

echo -e "${GREEN}Option 3: Mac/Linux (Terminal)${NC}"
echo "  cd backend"
echo "  bash run.sh"
echo "  # Visit: http://localhost:8000/docs"
echo ""

echo -e "${YELLOW}📚 Documentation:${NC}"
echo "  - README.md ................. Complete project documentation"
echo "  - GettingStarted.md ......... Original setup guide"
echo "  - Roadmap.md ................ Development roadmap"
echo "  - FIX_SUMMARY.md ............ All fixes applied"
echo ""

echo -e "${YELLOW}🔍 Verify Setup:${NC}"
echo "  cd backend"
echo "  python verify_setup.py"
echo ""

echo -e "${YELLOW}⚙️  Configuration:${NC}"
echo "  1. In backend folder, create .env file:"
echo "     cp ../.env.example .env"
echo "  2. Edit .env with your settings (database, API keys, etc.)"
echo ""

echo -e "${YELLOW}📝 Testing the API:${NC}"
echo "  Once backend is running, visit:"
echo "  http://localhost:8000/docs"
echo ""
echo "  This opens Swagger UI where you can:"
echo "  ✓ See all available endpoints"
echo "  ✓ Test endpoints with 'Try it out'"
echo "  ✓ See request/response examples"
echo ""

echo -e "${YELLOW}🐳 Docker Quick Commands:${NC}"
echo "  Start services:    docker-compose -f docker/docker-compose.yml up -d"
echo "  Stop services:     docker-compose -f docker/docker-compose.yml down"
echo "  View logs:         docker-compose -f docker/docker-compose.yml logs -f"
echo "  Shell into db:     docker exec -it citeguard-postgres psql -U citeguard"
echo ""

echo -e "${YELLOW}🧪 Database (PostgreSQL):${NC}"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  User: citeguard"
echo "  Password: citeguard"
echo "  Database: citeguard"
echo ""

echo -e "${YELLOW}💾 Cache (Redis):${NC}"
echo "  Host: localhost"
echo "  Port: 6379"
echo ""

echo -e "${YELLOW}📁 Project Structure:${NC}"
echo "  backend/           Python FastAPI backend"
echo "  ├── app/           Main application code"
echo "  │   ├── api/       API endpoints"
echo "  │   ├── core/      Configuration"
echo "  │   ├── services/  Business logic"
echo "  │   ├── models/    Database models"
echo "  │   └── schemas/   Request/response validation"
echo "  ├── requirements.txt  Python dependencies"
echo "  └── run.sh/.bat    Startup scripts"
echo ""
echo "  extension/         Chrome extension"
echo "  ├── manifest.json  Extension config"
echo "  ├── background.js  Service worker"
echo "  ├── content.js     Page injection"
echo "  └── popup.html     Main UI"
echo ""
echo "  docker/            Docker configuration"
echo "  ├── docker-compose.yml"
echo "  └── Dockerfile.backend"
echo ""

echo -e "${YELLOW}🔗 Important Links:${NC}"
echo "  API Documentation: http://localhost:8000/docs"
echo "  API Health: http://localhost:8000/health"
echo "  Root Endpoint: http://localhost:8000/"
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ All systems ready! Choose an option above to get started.${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
