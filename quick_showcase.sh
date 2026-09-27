#!/bin/bash

# Quick Showcase Script for AI Fair Lending Validation System
# This script helps you quickly set up and showcase the project

echo "🚀 AI Fair Lending Validation System - Quick Showcase Setup"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}❌ Python not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}❌ Node.js not found. Please install Node.js${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Function to start backend
start_backend() {
    echo -e "${BLUE}📦 Starting Backend Server...${NC}"
    cd backend
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    fi
    
    source venv/bin/activate 2>/dev/null || . venv/bin/activate 2>/dev/null
    pip install -r requirements.txt -q
    
    echo -e "${GREEN}✅ Backend dependencies installed${NC}"
    echo -e "${BLUE}🚀 Starting backend on http://localhost:8000${NC}"
    echo -e "${YELLOW}   (Press Ctrl+C to stop)${NC}"
    echo ""
    
    python -m uvicorn app.main:app --reload --port 8000
}

# Function to start frontend
start_frontend() {
    echo -e "${BLUE}📦 Starting Frontend Server...${NC}"
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi
    
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
    echo -e "${BLUE}🚀 Starting frontend on http://localhost:3000${NC}"
    echo -e "${YELLOW}   (Press Ctrl+C to stop)${NC}"
    echo ""
    
    npm run dev
}

# Function to show showcase steps
show_steps() {
    echo ""
    echo -e "${GREEN}📋 Quick Showcase Steps:${NC}"
    echo "============================================================"
    echo ""
    echo "1. Login (http://localhost:3000)"
    echo "   - Admin: EMP001 / admin123"
    echo "   - Analyst: EMP002 / analyst123"
    echo ""
    echo "2. Generate Profiles (200-300 profiles)"
    echo "   - Go to Profiles → Generate"
    echo "   - Select dimension (Rural vs Urban)"
    echo ""
    echo "3. Run Bias Analysis"
    echo "   - Go to Bias Analysis"
    echo "   - Select dimension → Run Analysis"
    echo ""
    echo "4. Provide Feedback"
    echo "   - Go to Feedback"
    echo "   - Submit expert feedback on detected bias"
    echo ""
    echo "5. Run Mitigation ⭐"
    echo "   - Go to Mitigation"
    echo "   - Run 5-7 iterations"
    echo "   - Show before/after improvements"
    echo ""
    echo -e "${BLUE}📖 Full guide: See SHOWCASE_GUIDE.md${NC}"
    echo ""
}

# Main menu
echo "Select an option:"
echo "1) Start Backend Server"
echo "2) Start Frontend Server"
echo "3) Start Both (requires 2 terminals)"
echo "4) Show Quick Showcase Steps"
echo "5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        start_backend
        ;;
    2)
        start_frontend
        ;;
    3)
        echo -e "${YELLOW}⚠️  Starting both requires 2 terminals${NC}"
        echo -e "${BLUE}Terminal 1: Backend, Terminal 2: Frontend${NC}"
        echo ""
        read -p "Continue? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            start_backend &
            sleep 2
            start_frontend
        fi
        ;;
    4)
        show_steps
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
