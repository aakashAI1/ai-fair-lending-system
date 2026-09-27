#!/bin/bash
# Cross-platform Setup Script for Fair Lending AI Validation
# Works on Mac and Linux

set -e  # Exit on error

echo "========================================"
echo "Fair Lending AI Validation - Setup"
echo "========================================"
echo ""

# Check Python
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi
python3 --version
echo ""

# Check Node.js
echo "[2/6] Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
node --version
echo ""

# Setup Backend
echo "[3/6] Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash
DEBUG=True
ENVIRONMENT=development
DATABASE_URL=sqlite:///./fairlending.db
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
EOF
    echo ".env file created. Please edit it and add your API keys."
fi
echo ""

# Setup Frontend
echo "[4/6] Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Node.js dependencies"
        exit 1
    fi
fi
echo ""

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi
echo ""

cd ..

# Create uploads directory
echo "[5/7] Creating uploads directory..."
mkdir -p backend/uploads
echo ""

# Populate database with sample data
echo "[6/7] Populating database with sample data..."
cd backend
source venv/bin/activate
python3 scripts/populate_mock_data.py
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to populate sample data. You can run it manually later:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python3 scripts/populate_mock_data.py"
else
    echo "[OK] Sample data populated successfully!"
fi
cd ..
echo ""

echo "[7/7] Setup complete!"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Edit backend/.env and add your Gemini API key:"
echo "   GEMINI_API_KEY=your-actual-api-key"
echo "   (Optional - only needed for GenAI profile generation)"
echo ""
echo "2. Start the backend server:"
echo "   ./start-backend.sh"
echo "   OR: cd backend && source venv/bin/activate && python3 -m uvicorn app.main:app --reload --port 8000"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   ./start-frontend.sh"
echo "   OR: cd frontend && npm run dev"
echo ""
echo "4. Open http://localhost:3000/dashboard in your browser"
echo "   You should see sample metrics and data!"
echo ""
echo "========================================"

