#!/bin/bash

# Restart script for Frontend (Next.js) application
# This script kills any existing Next.js processes and restarts the dev server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔄 Restarting Frontend Application...${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

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

# Kill any existing Next.js processes
echo -e "${YELLOW}Checking for existing Next.js processes...${NC}"

# Kill by port 3000 (default Next.js dev server port)
kill_port 3000

# Also kill any Node processes running Next.js (fallback)
NODE_PIDS=$(ps aux | grep -i "next dev\|next-server" | grep -v grep | awk '{print $2}' || true)
if [ -n "$NODE_PIDS" ]; then
    echo -e "${YELLOW}⚠️  Killing remaining Next.js processes...${NC}"
    echo "$NODE_PIDS" | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Optional: Clean .next cache (uncomment if needed)
# echo -e "${YELLOW}Cleaning .next cache...${NC}"
# rm -rf .next
# echo -e "${GREEN}✓ Cache cleaned${NC}"

# Wait a moment for processes to fully terminate
sleep 1

# Refresh environment variables from .env file
echo -e "${YELLOW}🔄 Refreshing environment variables from .env file...${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
    echo -e "${YELLOW}   Some environment variables may not be set${NC}"
else
    # Load environment variables from .env file
    set -a  # Automatically export all variables
    source .env 2>/dev/null || true
    set +a  # Disable automatic export
    
    # Verify NEXT_PUBLIC_API_URL is set
    if [ -z "$NEXT_PUBLIC_API_URL" ]; then
        echo -e "${YELLOW}⚠️  Warning: NEXT_PUBLIC_API_URL not found in .env file${NC}"
        echo -e "${YELLOW}   Defaulting to http://localhost:8000${NC}"
        export NEXT_PUBLIC_API_URL=http://localhost:8000
    else
        echo -e "${GREEN}✓ Environment variables loaded from .env file${NC}"
        export NEXT_PUBLIC_API_URL
    fi
fi

# Start the Next.js dev server
echo -e "${GREEN}🚀 Starting Next.js development server...${NC}"
echo -e "${GREEN}📍 Server will be available at: http://localhost:3000${NC}"
echo ""

# Start in background and capture PID
npm run dev &
FRONTEND_PID=$!

# Wait a moment to check if it started successfully
sleep 3

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Frontend application restarted successfully!${NC}"
    echo -e "${GREEN}   Process ID: $FRONTEND_PID${NC}"
    echo -e "${GREEN}   Running at: http://localhost:3000${NC}"
    echo ""
    echo -e "${YELLOW}To stop the server, press Ctrl+C or run: kill $FRONTEND_PID${NC}"
else
    echo -e "${RED}❌ Failed to start frontend application${NC}"
    exit 1
fi

