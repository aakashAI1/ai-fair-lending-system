#!/bin/bash
# Start Frontend Server (Mac/Linux)

echo "Starting Fair Lending AI Validation Frontend..."
echo ""

cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "ERROR: Dependencies not installed!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Start development server
echo "Starting frontend server on http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""
npm run dev

