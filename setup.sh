#!/bin/bash

# AI Video Studio - Quick Setup Script
# This script helps you set up the project quickly

echo "🎬 AI Video Studio - Quick Setup"
echo "================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env exists in backend
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your GROQ_API_KEY"
    echo "   Get your free API key from: https://groq.com"
    echo ""
    
    # Ask user if they want to add the key now
    read -p "Do you have your Groq API key ready? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Groq API key: " groq_key
        sed -i "s/your_groq_api_key_here/$groq_key/" backend/.env
        echo "✅ Groq API key added to backend/.env"
    else
        echo "⚠️  Don't forget to add your Groq API key to backend/.env before running!"
    fi
else
    echo "✅ backend/.env already exists"
fi

echo ""

# Check if .env exists in root
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    
    if [ -f "backend/.env" ]; then
        # Try to copy GROQ_API_KEY from backend/.env
        groq_key=$(grep GROQ_API_KEY backend/.env | cut -d '=' -f2)
        if [ ! -z "$groq_key" ] && [ "$groq_key" != "your_groq_api_key_here" ]; then
            echo "GROQ_API_KEY=$groq_key" >> .env
            echo "✅ Copied Groq API key to .env"
        fi
    fi
else
    echo "✅ .env already exists"
fi

echo ""
echo "🚀 Setup complete!"
echo ""
echo "To start the application:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop the application:"
echo "  docker-compose down"
echo ""
echo "Access the application at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
