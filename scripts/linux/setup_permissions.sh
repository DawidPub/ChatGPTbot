#!/bin/bash

# ChatGPT Bot - Set Permissions Script
# This script sets proper permissions for all files in the project

echo "🔧 Setting proper file permissions for ChatGPT Bot..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Set executable permissions for shell scripts
echo -e "${YELLOW}📄 Setting executable permissions for shell scripts...${NC}"
chmod +x *.sh
echo "✅ Shell scripts (.sh) - executable"

# Set readable permissions for Python files
echo -e "${YELLOW}📄 Setting permissions for Python files...${NC}"
chmod 644 *.py
echo "✅ Python files (.py) - readable/writable"

# Set readable permissions for documentation
echo -e "${YELLOW}📄 Setting permissions for documentation...${NC}"
chmod 644 *.md
echo "✅ Documentation files (.md) - readable"

# Set permissions for configuration files
echo -e "${YELLOW}📄 Setting permissions for configuration files...${NC}"
chmod 644 requirements.txt
chmod 644 Dockerfile
chmod 644 docker-compose.yml
chmod 644 Makefile 2>/dev/null || echo "⚠️ Makefile not found, skipping"
echo "✅ Configuration files - readable"

# Set permissions for batch files
echo -e "${YELLOW}📄 Setting permissions for Windows batch files...${NC}"
chmod 644 *.bat
echo "✅ Batch files (.bat) - readable"

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    echo -e "${YELLOW}📁 Creating data directory...${NC}"
    mkdir -p data
    chmod 755 data
    echo "✅ Data directory created"
fi

# Set permissions for data directory
chmod 755 data 2>/dev/null || echo "⚠️ Data directory not found, skipping"

# Set permissions for cache directories
echo -e "${YELLOW}📁 Setting permissions for cache directories...${NC}"
chmod -R 755 __pycache__ 2>/dev/null || echo "ℹ️ No __pycache__ directory found"
chmod -R 755 .pytest_cache 2>/dev/null || echo "ℹ️ No .pytest_cache directory found"

# Special files that might need different permissions
echo -e "${YELLOW}🔐 Setting permissions for special files...${NC}"
chmod 600 *.pkl 2>/dev/null || echo "ℹ️ No pickle files found"
chmod 600 *.json 2>/dev/null || echo "ℹ️ No JSON session files found"

echo ""
echo "============================================================"
echo -e "${GREEN}✅ Permissions set successfully!${NC}"
echo "============================================================"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "  • Shell scripts (.sh): executable (755)"
echo "  • Python files (.py): readable/writable (644)"
echo "  • Documentation (.md): readable (644)"
echo "  • Config files: readable (644)"
echo "  • Data directory: accessible (755)"
echo "  • Session files: private (600)"
echo ""
echo -e "${BLUE}🚀 You can now run:${NC}"
echo "  ./run_chatgpt_api.sh"
echo "  ./install_all_dependencies.sh"
echo "  make help"
echo ""
