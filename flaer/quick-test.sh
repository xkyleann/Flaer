#!/bin/bash

# Flaer SaaS Quick Test Script
# This script helps you quickly test the SaaS platform

set -e

echo "🚀 Flaer SaaS Quick Test Script"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Error: Please run this script from the flaer directory${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Setting up backend...${NC}"
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
DATABASE_URL=sqlite:///./test_flaer.db
JWT_SECRET_KEY=test-secret-key-for-development-only
STRIPE_SECRET_KEY=sk_test_dummy
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
EOF
    echo -e "${GREEN}✅ Created .env file${NC}"
fi

# Initialize database
echo "Initializing database..."
python3 << EOF
from database import init_db
try:
    init_db()
    print("✅ Database initialized successfully!")
except Exception as e:
    print(f"⚠️  Database might already exist: {e}")
EOF

echo ""
echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo ""
echo -e "${BLUE}Step 2: Testing API endpoints...${NC}"

# Start server in background
echo "Starting backend server..."
uvicorn main:app --port 5001 > /dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:5001/api/health)
if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
fi

# Test root endpoint
echo "Testing root endpoint..."
ROOT_RESPONSE=$(curl -s http://localhost:5001/)
if echo "$ROOT_RESPONSE" | grep -q "Flaer"; then
    echo -e "${GREEN}✅ Root endpoint working${NC}"
else
    echo -e "${RED}❌ Root endpoint failed${NC}"
fi

# Test login with demo user
echo "Testing authentication..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5001/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@flaer.io","password":"Test@2026!"}')

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ Authentication working${NC}"
    
    # Extract token
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    
    # Test protected endpoint
    echo "Testing protected endpoint..."
    DASHBOARD_RESPONSE=$(curl -s http://localhost:5001/api/dashboard/overview \
        -H "Authorization: Bearer $TOKEN")
    
    if echo "$DASHBOARD_RESPONSE" | grep -q "health_score"; then
        echo -e "${GREEN}✅ Protected endpoints working${NC}"
    else
        echo -e "${RED}❌ Protected endpoint failed${NC}"
    fi
else
    echo -e "${RED}❌ Authentication failed${NC}"
fi

# Stop server
kill $SERVER_PID 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "📚 Next steps:"
echo "  1. Start backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload --port 5001"
echo "  2. Start frontend: cd frontend-svelte && npm install && npm run dev"
echo "  3. Visit: http://localhost:5173"
echo ""
echo "📖 Documentation:"
echo "  - Setup Guide: SAAS_SETUP.md"
echo "  - Testing Guide: SAAS_TESTING_GUIDE.md"
echo "  - Implementation Guide: SAAS_IMPLEMENTATION_GUIDE.md"
echo ""
echo "🎉 Happy coding!"

# Made with Bob
