#!/bin/bash

# AIrth Platform Launcher
# Professional Sustainability Intelligence Platform

echo "========================================================================"
echo "🌍 Starting AIrth Platform"
echo "========================================================================"
echo ""
echo "📦 Checking dependencies..."

# if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "✓ Python found: $($PYTHON_CMD --version)"
echo ""
echo "🚀 Launching application..."
echo ""

# Run the application
cd "$(dirname "$0")"
$PYTHON_CMD src/app.py

