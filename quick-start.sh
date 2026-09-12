#!/bin/bash

# flaer Quick Start Script
# Starts both backend and frontend for testing

echo "🚀 Starting flaer..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "flaer/backend" ] || [ ! -d "flaer/frontend-svelte" ]; then
    echo "❌ Please run this script from the AIrth directory"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Install backend dependencies if needed
echo "📦 Checking backend dependencies..."
cd flaer/backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

pip3 install -q -r requirements.txt
echo "✅ Backend dependencies ready"
echo ""

# Initialize database if needed
if [ ! -f "flaer.db" ]; then
    echo "🗄️  Initializing database..."
    python3 init_database.py
    echo "✅ Database initialized"
    echo ""
fi

# Start backend in background
echo "🔧 Starting backend server..."
python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)"
echo ""

# Install frontend dependencies if needed
cd ../frontend-svelte
echo "📦 Checking frontend dependencies..."
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
fi
echo "✅ Frontend dependencies ready"
echo ""

# Start frontend
echo "🎨 Starting frontend server..."
echo "✅ Frontend will run on http://localhost:5173"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 flaer is ready!"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

trap cleanup INT TERM

# Start frontend (this will block)
npm run dev

# If npm run dev exits, cleanup
cleanup

# Made with Bob
