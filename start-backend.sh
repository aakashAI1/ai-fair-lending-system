#!/bin/bash
# Start Backend Server (Mac/Linux)

echo "Starting Fair Lending AI Validation Backend..."
echo ""

cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please create .env file with your API keys."
    exit 1
fi

# Start server
echo "Starting backend server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

