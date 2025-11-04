#!/bin/bash

# Restart script for both Frontend and Backend applications
# This script kills existing processes and restarts both applications

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🔄 Restarting Both Frontend and Backend Applications${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to kill processes on a specific port
kill_port() {
    local port=$1
    local name=$2
    local pids=$(lsof -ti:$port 2>/dev/null || true)
    
    if [ -n "$pids" ]; then
        echo -e "${YELLOW}⚠️  Killing $name processes on port $port...${NC}"
        echo "$pids" | xargs kill -9 2>/dev/null || true
        sleep 1
    else
        echo -e "${GREEN}✓ No $name processes found on port $port${NC}"
    fi
}

# Kill all existing processes
echo -e "${YELLOW}📋 Stopping existing processes...${NC}"
echo ""

# Kill frontend (port 3000)
kill_port 3000 "Next.js"

# Kill backend (port 8000)
kill_port 8000 "FastAPI"

# Also kill any remaining Node.js processes running Next.js
NODE_PIDS=$(ps aux | grep -i "next dev\|next-server" | grep -v grep | awk '{print $2}' || true)
if [ -n "$NODE_PIDS" ]; then
    echo -e "${YELLOW}⚠️  Killing remaining Next.js processes...${NC}"
    echo "$NODE_PIDS" | xargs kill -9 2>/dev/null || true
fi

# Kill any remaining uvicorn processes
UVICORN_PIDS=$(ps aux | grep -i uvicorn | grep -v grep | awk '{print $2}' || true)
if [ -n "$UVICORN_PIDS" ]; then
    echo -e "${YELLOW}⚠️  Killing remaining uvicorn processes...${NC}"
    echo "$UVICORN_PIDS" | xargs kill -9 2>/dev/null || true
fi

# Wait for processes to fully terminate
sleep 2

# Refresh AWS credentials from backend .env file
echo -e "${YELLOW}🔄 Refreshing AWS credentials from backend/.env file...${NC}"

if [ -f "backend/.env" ]; then
    # Load backend environment variables
    set -a  # Automatically export all variables
    source backend/.env 2>/dev/null || true
    set +a  # Disable automatic export
    
    # Verify AWS credentials are set
    if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
        echo -e "${YELLOW}⚠️  Warning: AWS credentials not found in backend/.env file${NC}"
        echo -e "${YELLOW}   Please ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set${NC}"
    else
        echo -e "${GREEN}✓ AWS credentials loaded from backend/.env file${NC}"
        export AWS_ACCESS_KEY_ID
        export AWS_SECRET_ACCESS_KEY
        export AWS_REGION
        export AWS_BEDROCK_MODEL
    fi
else
    echo -e "${YELLOW}⚠️  Warning: backend/.env file not found${NC}"
fi

# Refresh frontend environment variables
echo -e "${YELLOW}🔄 Refreshing environment variables from frontend/.env file...${NC}"

if [ -f "frontend/.env" ]; then
    # Load frontend environment variables
    set -a  # Automatically export all variables
    source frontend/.env 2>/dev/null || true
    set +a  # Disable automatic export
    
    if [ -z "$NEXT_PUBLIC_API_URL" ]; then
        echo -e "${YELLOW}⚠️  Warning: NEXT_PUBLIC_API_URL not found in frontend/.env file${NC}"
    else
        echo -e "${GREEN}✓ Frontend environment variables loaded${NC}"
        export NEXT_PUBLIC_API_URL
    fi
else
    echo -e "${YELLOW}⚠️  Warning: frontend/.env file not found${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🚀 Starting Backend Application${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Start backend first (it takes longer to initialize)
if [ -f "backend/restart_backend.sh" ]; then
    # Run backend restart script in a new terminal window if possible, otherwise in background
    bash backend/restart_backend.sh &
    BACKEND_PID=$!
else
    echo -e "${RED}❌ Backend restart script not found!${NC}"
    exit 1
fi

# Wait a moment for backend to start
sleep 3

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🚀 Starting Frontend Application${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Start frontend
if [ -f "frontend/restart_frontend.sh" ]; then
    # Run frontend restart script in a new terminal window if possible, otherwise in background
    bash frontend/restart_frontend.sh &
    FRONTEND_PID=$!
else
    echo -e "${RED}❌ Frontend restart script not found!${NC}"
    exit 1
fi

# Wait for both to initialize
sleep 3

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Both applications restarted successfully!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}📍 Backend:${NC}"
echo -e "   URL: http://localhost:8000"
echo -e "   API Docs: http://localhost:8000/docs"
echo -e "   Health: http://localhost:8000/health"
echo ""
echo -e "${GREEN}📍 Frontend:${NC}"
echo -e "   URL: http://localhost:3000"
echo ""
echo -e "${YELLOW}💡 Note: Applications are running in the background${NC}"
echo -e "${YELLOW}   To stop them, use:${NC}"
echo -e "   - kill $BACKEND_PID  (Backend)"
echo -e "   - kill $FRONTEND_PID (Frontend)"
echo -e "   - Or use: pkill -f 'uvicorn app.main:app'  (Backend)"
echo -e "   - Or use: pkill -f 'next dev'  (Frontend)"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

