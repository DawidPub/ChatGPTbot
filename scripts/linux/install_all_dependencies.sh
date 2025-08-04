#!/bin/bash

echo "============================================================"
echo "       📦 ChatGPT Bot - Complete Dependencies Install"
echo "============================================================"
echo ""
echo "Installing ALL required packages from requirements.txt..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found!${NC}"
    echo "Make sure you're in the correct directory."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python not found${NC}"
        echo "Please install Python 3.7+ first:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
        echo "  Fedora:        sudo dnf install python3 python3-pip"
        echo "  Arch:          sudo pacman -S python python-pip"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}❌ pip not found${NC}"
    echo "Please install pip:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  Or: curl https://bootstrap.pypa.io/get-pip.py | $PYTHON_CMD"
    exit 1
fi

echo -e "${BLUE}🐍 Using Python: $($PYTHON_CMD --version)${NC}"
echo ""

echo "📋 Current requirements.txt contents:"
echo "============================================================"
cat requirements.txt
echo "============================================================"
echo ""

echo -e "${BLUE}🚀 Starting installation...${NC}"
echo ""

# Upgrade pip first
echo -e "${YELLOW}📦 Upgrading pip...${NC}"
$PYTHON_CMD -m pip install --upgrade pip

# Install all packages from requirements.txt
echo ""
echo -e "${YELLOW}📦 Installing packages from requirements.txt...${NC}"
$PYTHON_CMD -m pip install -r requirements.txt

# Check installation
echo ""
echo -e "${BLUE}🔍 Verifying installation...${NC}"
$PYTHON_CMD -c "
import sys
packages = ['selenium', 'webdriver_manager', 'fastapi', 'uvicorn', 'pydantic', 'requests']
failed = []
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg} - OK')
    except ImportError:
        print(f'❌ {pkg} - FAILED')
        failed.append(pkg)

if failed:
    print(f'\n❌ Failed packages: {failed}')
    sys.exit(1)
else:
    print('\n🎉 All core packages installed successfully!')
"

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Some packages failed to install or import${NC}"
    echo -e "${YELLOW}💡 Try running: $PYTHON_CMD -m pip install --upgrade --force-reinstall -r requirements.txt${NC}"
    exit 1
fi

echo ""
echo "============================================================"
echo "                    🎉 Installation Complete!"
echo "============================================================"
echo ""
echo -e "${GREEN}✅ All packages installed successfully!${NC}"
echo ""
echo -e "${BLUE}🚀 You can now run:${NC}"
echo "  • ./run_chatgpt_api.sh - Full API system"
echo "  • ./run_chatgpt_bot_working.sh - Original bot"
echo "  • python3 chatgpt_api_launcher.py - API launcher GUI"
echo ""
echo -e "${BLUE}📖 For more info see:${NC}"
echo "  • README_API.md - API documentation"
echo "  • INSTALL.md - Detailed installation guide"
echo ""
echo "Press Enter to continue..."
read
