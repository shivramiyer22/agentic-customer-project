#!/bin/bash

# Restart script for Backend (FastAPI) application
# This script kills any existing uvicorn processes and restarts the server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔄 Restarting Backend Application...${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}   Please create a virtual environment first:${NC}"
    echo -e "   python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
source venv/bin/activate

# Verify activation
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Function to kill processes on a specific port
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null || true)
    
    if [ -n "$pids" ]; then
        echo -e "${YELLOW}⚠️  Killing processes on port $port...${NC}"
        echo "$pids" | xargs kill -9 2>/dev/null || true
        sleep 1
    else
        echo -e "${GREEN}✓ No processes found on port $port${NC}"
    fi
}

# Kill any existing uvicorn processes
echo -e "${YELLOW}Checking for existing uvicorn processes...${NC}"

# Kill by port 8000 (default FastAPI port)
kill_port 8000

# Also kill any uvicorn processes (fallback)
UVICORN_PIDS=$(ps aux | grep -i uvicorn | grep -v grep | awk '{print $2}' || true)
if [ -n "$UVICORN_PIDS" ]; then
    echo -e "${YELLOW}⚠️  Killing remaining uvicorn processes...${NC}"
    echo "$UVICORN_PIDS" | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Wait a moment for processes to fully terminate
sleep 1

# Refresh AWS credentials from .env file
echo -e "${YELLOW}🔄 Refreshing AWS credentials from .env file...${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
    echo -e "${YELLOW}   Some environment variables may not be set${NC}"
else
    # Load AWS credentials from .env file
    # Source .env file and export AWS credentials
    set -a  # Automatically export all variables
    source .env 2>/dev/null || true
    set +a  # Disable automatic export
    
    # Verify AWS credentials are set
    if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
        echo -e "${YELLOW}⚠️  Warning: AWS credentials not found in .env file${NC}"
        echo -e "${YELLOW}   Please ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set${NC}"
    else
        echo -e "${GREEN}✓ AWS credentials loaded from .env file${NC}"
        # Export credentials explicitly
        export AWS_ACCESS_KEY_ID
        export AWS_SECRET_ACCESS_KEY
        export AWS_REGION
        export AWS_BEDROCK_MODEL
    fi
fi

# Start the FastAPI server
echo -e "${GREEN}🚀 Starting FastAPI server...${NC}"
echo -e "${GREEN}📍 Server will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}📍 API Docs will be available at: http://localhost:8000/docs${NC}"
echo ""

# Start in background and capture PID
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment to check if it started successfully
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Backend application restarted successfully!${NC}"
    echo -e "${GREEN}   Process ID: $BACKEND_PID${NC}"
    echo -e "${GREEN}   Running at: http://localhost:8000${NC}"
    echo -e "${GREEN}   API Docs: http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${YELLOW}To stop the server, press Ctrl+C or run: kill $BACKEND_PID${NC}"
else
    echo -e "${RED}❌ Failed to start backend application${NC}"
    exit 1
fi

