#!/bin/bash

echo "============================================================"
echo "         📦 Installing ChatGPT Bot API Dependencies"
echo "============================================================"
echo ""
echo "Installing required packages for FastAPI server and client..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found${NC}"
    echo "Please install Python 3.7+ first"
    exit 1
fi

echo -e "${BLUE}🐍 Using Python: $($PYTHON_CMD --version)${NC}"
echo ""

# Check if pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}❌ pip not found${NC}"
    echo "Please install pip first"
    exit 1
fi

echo -e "${YELLOW}📦 Installing API packages...${NC}"
$PYTHON_CMD -m pip install --upgrade pip

# Install specific API packages
$PYTHON_CMD -m pip install "fastapi>=0.100.0" "uvicorn>=0.20.0" "pydantic>=2.0.0" "requests>=2.28.0"

echo ""
echo -e "${GREEN}✅ Installation completed!${NC}"
echo ""
echo -e "${BLUE}📋 Installed packages:${NC}"
echo "  ✅ fastapi - Web framework for building APIs"
echo "  ✅ uvicorn - ASGI server for running FastAPI"
echo "  ✅ pydantic - Data validation using Python type hints"
echo "  ✅ requests - HTTP library for API client"
echo ""
echo -e "${BLUE}🚀 You can now run:${NC}"
echo "  • ./run_chatgpt_api.sh - Full launcher with menu"
echo "  • python3 chatgpt_api_server.py - API server only"
echo "  • python3 chatgpt_api_client.py - API client only"
echo ""
echo "Press Enter to continue..."
read
