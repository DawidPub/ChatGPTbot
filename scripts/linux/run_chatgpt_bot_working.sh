#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================================"
echo "          🚀 ChatGPT Bot - WORKING VERSION 🚀"
echo "============================================================"
echo ""
echo "Starting ChatGPT Bot with all dependencies resolved..."
echo ""
echo -e "${BLUE}💡 Features included:${NC}"
echo "  ✅ Complete GUI interface (tkinter)"
echo "  ✅ Full selenium automation support (v4.34.2+)"
echo "  ✅ webdriver-manager for Chrome automation"
echo "  ✅ All local modules (chatgpt_gui, chatgpt_bot_core)"
echo "  ✅ All standard Python modules (json, pickle, os, time)"
echo ""
echo "If the application doesn't start, please check:"
echo "1. Chrome/Chromium browser is installed"
echo "2. You have internet connection"
echo "3. Required Python packages are installed"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.7+${NC}"
    exit 1
fi

echo -e "${YELLOW}Starting in 3 seconds...${NC}"
sleep 3
echo ""

# Check if main.py exists, otherwise try chatgpt_gui.py
if [ -f "main.py" ]; then
    echo -e "${GREEN}🚀 Launching ChatGPT Bot (main.py)...${NC}"
    $PYTHON_CMD main.py
elif [ -f "chatgpt_gui.py" ]; then
    echo -e "${GREEN}🚀 Launching ChatGPT Bot (chatgpt_gui.py)...${NC}"
    $PYTHON_CMD chatgpt_gui.py
else
    echo -e "${RED}❌ Could not find main.py or chatgpt_gui.py${NC}"
    echo "Please make sure you're in the correct directory."
    exit 1
fi

echo ""
echo -e "${GREEN}✅ ChatGPT Bot finished!${NC}"
echo ""
echo "If you encountered any errors, try:"
echo "1. ./install_all_dependencies.sh"
echo "2. ./check_dependencies.sh"
echo ""
echo "Press Enter to exit..."
read
