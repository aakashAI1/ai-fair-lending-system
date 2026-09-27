#!/bin/bash

# Script to train ML model and run the project

echo "============================================================"
echo "Fair Lending AI Validation - ML Model Training and Setup"
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
echo "Training ML model on real datasets..."
echo "This will:"
echo "  1. Import both datasets"
echo "  2. Train ML model"
echo "  3. Score all profiles"
echo "  4. Calculate bias metrics"
echo ""
echo "This may take a few minutes..."
echo ""

python scripts/train_ml_model.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "ML Model Training Complete!"
    echo "============================================================"
    echo ""
    echo "Next steps:"
    echo "  1. Start backend: ./start-backend.sh (in a new terminal)"
    echo "  2. Start frontend: ./start-frontend.sh (in another terminal)"
    echo "  3. Open http://localhost:3000/dashboard"
    echo ""
    echo "Your dashboard will show metrics from the trained ML model!"
    echo ""
else
    echo ""
    echo "Error occurred during training. Please check the error messages above."
    exit 1
fi

