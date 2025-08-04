#!/bin/bash

echo "============================================================"
echo "       🔍 ChatGPT Bot - Check Installed Packages"
echo "============================================================"
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
    echo -e "${RED}❌ Python not found in PATH${NC}"
    exit 1
fi

echo -e "${BLUE}🐍 Python version:${NC}"
$PYTHON_CMD --version
echo ""

echo -e "${YELLOW}📦 Checking installed packages...${NC}"
echo "============================================================"

# Create temporary Python script to check packages
cat > check_packages.py << 'EOF'
import sys

packages = [
    ('selenium', 'selenium'),
    ('webdriver-manager', 'webdriver_manager'),
    ('fastapi', 'fastapi'),
    ('uvicorn', 'uvicorn'),
    ('pydantic', 'pydantic'),
    ('requests', 'requests'),
    ('pyinstaller', 'PyInstaller'),
    ('pytest', 'pytest'),
    ('black', 'black'),
    ('flake8', 'flake8'),
    ('python-multipart', 'multipart'),
    ('aiofiles', 'aiofiles')
]

installed = []
missing = []

for display_name, import_name in packages:
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f'✅ {display_name:<20} {version}')
        installed.append(display_name)
    except ImportError:
        print(f'❌ {display_name:<20} NOT INSTALLED')
        missing.append(display_name)

print()
print('============================================================')
print(f'📊 Summary: {len(installed)} installed, {len(missing)} missing')

if missing:
    print('❌ Missing packages:', ', '.join(missing))
    print('💡 Run: pip install ' + ' '.join(missing))
    print('💡 Or run: ./install_all_dependencies.sh')
else:
    print('🎉 All packages are installed!')
EOF

# Run the check
$PYTHON_CMD check_packages.py

# Clean up
rm -f check_packages.py

echo ""
echo "============================================================"
echo ""
echo -e "${BLUE}💡 Available installation options:${NC}"
echo "  • ./install_all_dependencies.sh - Install all packages"
echo "  • ./install_api_dependencies.sh - Install API packages only"
echo "  • pip install -r requirements.txt - Manual installation"
echo ""
echo "Press Enter to continue..."
read
