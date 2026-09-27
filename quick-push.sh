#!/bin/bash
# Quick Push Script for GitHub
# Usage: ./quick-push.sh

echo "========================================"
echo "Quick GitHub Push"
echo "========================================"
echo ""

echo "[1/4] Checking git status..."
git status
echo ""

echo "[2/4] Pulling latest changes..."
git pull
if [ $? -ne 0 ]; then
    echo "WARNING: Pull failed. Continue anyway? (y/n)"
    read -r continue
    if [ "$continue" != "y" ] && [ "$continue" != "Y" ]; then
        exit 1
    fi
fi
echo ""

echo "[3/4] Adding all changes..."
git add .
echo ""

echo "[4/4] Enter commit message:"
read -r message
if [ -z "$message" ]; then
    echo "ERROR: Commit message cannot be empty"
    exit 1
fi

git commit -m "$message"
if [ $? -ne 0 ]; then
    echo "ERROR: Commit failed"
    exit 1
fi
echo ""

echo "Pushing to GitHub..."
git push
if [ $? -ne 0 ]; then
    echo "ERROR: Push failed"
    exit 1
fi

echo ""
echo "========================================"
echo "SUCCESS! Changes pushed to GitHub"
echo "========================================"

