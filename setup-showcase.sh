#!/bin/bash

# Setup script for Mac/Linux to generate showcase data

echo "============================================================"
echo "Fair Lending AI Validation - Showcase Data Setup"
echo "============================================================"
echo ""

cd backend

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

echo ""
echo "Generating showcase data..."
echo "This may take a few minutes..."
echo ""

python scripts/setup_showcase_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "Setup complete! Your dashboard is ready for showcase."
    echo "============================================================"
    echo ""
    echo "Next steps:"
    echo "  1. Make sure backend is running: ./start-backend.sh"
    echo "  2. Make sure frontend is running: ./start-frontend.sh"
    echo "  3. Open http://localhost:3000/dashboard"
    echo ""
else
    echo ""
    echo "Error occurred during setup. Please check the error messages above."
    exit 1
fi

