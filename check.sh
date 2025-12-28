#!/bin/bash

# AI Video Studio - System Check Script
# Verifies that everything is set up correctly

echo "🎬 AI Video Studio - System Check"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo "1. Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    docker --version
else
    echo -e "${RED}✗${NC} Docker is NOT installed"
    echo "   Please install Docker: https://docs.docker.com/get-docker/"
fi
echo ""

# Check Docker Compose
echo "2. Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker Compose is installed"
    docker-compose --version
else
    echo -e "${RED}✗${NC} Docker Compose is NOT installed"
    echo "   Please install Docker Compose: https://docs.docker.com/compose/install/"
fi
echo ""

# Check backend .env
echo "3. Checking backend configuration..."
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} backend/.env exists"
    
    # Check for GROQ_API_KEY
    if grep -q "GROQ_API_KEY=gsk_" backend/.env; then
        echo -e "${GREEN}✓${NC} GROQ_API_KEY is configured"
    elif grep -q "GROQ_API_KEY=your_groq_api_key_here" backend/.env; then
        echo -e "${YELLOW}⚠${NC} GROQ_API_KEY needs to be set"
        echo "   Edit backend/.env and add your Groq API key"
    else
        echo -e "${RED}✗${NC} GROQ_API_KEY not found in backend/.env"
    fi
else
    echo -e "${YELLOW}⚠${NC} backend/.env not found"
    echo "   Run: cp backend/.env.example backend/.env"
fi
echo ""

# Check if containers are running
echo "4. Checking Docker containers..."
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓${NC} Containers are running"
    docker-compose ps
else
    echo -e "${YELLOW}⚠${NC} Containers are not running"
    echo "   Run: docker-compose up -d"
fi
echo ""

# Check endpoints
echo "5. Checking service endpoints..."

# Backend health check
if curl -s -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend is responding (http://localhost:8000)"
else
    echo -e "${YELLOW}⚠${NC} Backend is not responding yet"
    echo "   Wait a moment and try: curl http://localhost:8000/api/v1/health"
fi

# Frontend check
if curl -s -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend is responding (http://localhost:3000)"
else
    echo -e "${YELLOW}⚠${NC} Frontend is not responding yet"
    echo "   Wait a moment and try: curl http://localhost:3000"
fi
echo ""

# Summary
echo "=================================="
echo "Summary:"
echo ""
echo "Backend API:     http://localhost:8000"
echo "API Docs:        http://localhost:8000/docs"
echo "Frontend:        http://localhost:3000"
echo ""
echo "To start:        docker-compose up -d"
echo "To stop:         docker-compose down"
echo "To view logs:    docker-compose logs -f"
echo ""
echo "Need help? Check QUICKSTART.md or README.md"
echo ""
