# 📦 Installation Guide

## 🎯 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Stable connection required

### Recommended Requirements
- **Python**: 3.9 or higher
- **RAM**: 8GB or more
- **CPU**: Multi-core processor
- **Browser**: Chrome 90+ or Chromium

## 🚀 Quick Installation

### Method 1: Automated Installation (Recommended)

#### Windows
```batch
# Download and run installer
curl -O https://raw.githubusercontent.com/your-repo/chatgpt-bot/main/install.bat
install.bat
```

#### Linux/macOS
```bash
# Download and run installer
curl -O https://raw.githubusercontent.com/your-repo/chatgpt-bot/main/install.sh
chmod +x install.sh
./install.sh
```

### Method 2: Manual Installation

#### Step 1: Clone Repository
```bash
git clone https://github.com/your-repo/chatgpt-bot.git
cd chatgpt-bot
```

#### Step 2: Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Or use make (if available)
make install
```

#### Step 3: Verify Installation
```bash
# Test imports
python -c "import selenium, fastapi, tkinter; print('✅ All dependencies installed')"

# Run quick test
python test/test_imports.py
```

## 🔧 Detailed Installation Steps

### 1. Python Installation

#### Windows
```bash
# Download Python from python.org
# Or use Chocolatey
choco install python

# Or use winget
winget install Python.Python.3.9
```

#### macOS
```bash
# Using Homebrew
brew install python@3.9

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# For CentOS/RHEL
sudo yum install python3 python3-pip
```

### 2. Chrome/Chromium Installation

#### Windows
```bash
# Download from google.com/chrome
# Or use Chocolatey
choco install googlechrome
```

#### macOS
```bash
# Download from google.com/chrome
# Or use Homebrew
brew install --cask google-chrome
```

#### Linux
```bash
# Ubuntu/Debian
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable

# Or install Chromium
sudo apt install chromium-browser
```

### 3. Project Dependencies

#### Core Dependencies
```bash
# Install from requirements.txt
pip install -r requirements.txt
```

#### Manual Installation
```bash
# Core automation
pip install selenium>=4.0.0
pip install webdriver-manager>=3.8.0

# API system
pip install fastapi>=0.100.0
pip install uvicorn>=0.20.0
pip install pydantic>=2.0.0
pip install requests>=2.28.0

# Development tools
pip install pyinstaller>=6.0.0
pip install pytest>=7.0.0
```

## 🐳 Docker Installation

### Prerequisites
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Docker Setup
```bash
# Clone repository
git clone https://github.com/your-repo/chatgpt-bot.git
cd chatgpt-bot

# Build and run
docker-compose up -d

# Verify installation
curl http://localhost:8008/health
```

## 🛠️ Installation Scripts

### Windows Installation Script (`install.bat`)
```batch
@echo off
echo ============================================================
echo        📦 ChatGPT Bot - Windows Installation
echo ============================================================

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+
    echo Download from: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip not found. Please reinstall Python with pip
    pause
    exit /b 1
)

echo ✅ pip found

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!

REM Test installation
echo 🧪 Testing installation...
python test/test_imports.py

if errorlevel 1 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)

echo ============================================================
echo                    🎉 Installation Complete!
echo ============================================================
echo.
echo 🚀 You can now run:
echo   • python main.py - Desktop application
echo   • python chatgpt_api_server.py - API server
echo   • python chatgpt_api_launcher.py - API launcher
echo.
pause
```

### Linux/macOS Installation Script (`install.sh`)
```bash
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}        📦 ChatGPT Bot - Linux/macOS Installation${NC}"
echo -e "${BLUE}============================================================${NC}"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.7+${NC}"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "macOS: brew install python@3.9"
    exit 1
fi

echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found. Please install pip${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 found${NC}"

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment created and activated${NC}"
fi

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies installed successfully!${NC}"

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
python3 test/test_imports.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi

echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}                    🎉 Installation Complete!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "${GREEN}🚀 You can now run:${NC}"
echo "  • python3 main.py - Desktop application"
echo "  • python3 chatgpt_api_server.py - API server"
echo "  • python3 chatgpt_api_launcher.py - API launcher"
echo ""
echo -e "${YELLOW}💡 Tip: If you created a virtual environment, remember to activate it:${NC}"
echo "  source venv/bin/activate"
echo ""
```

## 🔍 Verification & Testing

### Basic Verification
```bash
# Test Python imports
python -c "
import selenium
import fastapi
import tkinter
import requests
print('✅ All core dependencies available')
"

# Test WebDriver
python -c "
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
print('✅ WebDriver setup working')
"
```

### Comprehensive Testing
```bash
# Run all tests
python -m pytest test/ -v

# Test specific components
python test/test_imports.py
python test/test_api.py
python test/test_modular.py
```

### Manual Testing
```bash
# Test desktop application
python main.py

# Test API server
python chatgpt_api_server.py
# In another terminal:
curl http://localhost:8008/health

# Test API launcher
python chatgpt_api_launcher.py
```

## 🚨 Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Windows
# Add Python to PATH or reinstall with "Add to PATH" option

# Linux/macOS
# Install Python 3.7+
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python@3.9               # macOS
```

#### Chrome/ChromeDriver Issues
```bash
# Update Chrome to latest version
# Or install Chromium
sudo apt install chromium-browser  # Linux

# Clear WebDriver cache
rm -rf ~/.wdm  # Linux/macOS
rmdir /s %USERPROFILE%\.wdm  # Windows
```

#### Permission Issues (Linux/macOS)
```bash
# Fix permissions
chmod +x *.sh
sudo chown -R $USER:$USER .

# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Network Issues
```bash
# Use proxy if needed
pip install -r requirements.txt --proxy http://proxy:port

# Or configure pip
pip config set global.proxy http://proxy:port
```

### Getting Help

#### Check Logs
```bash
# Enable debug mode
export DEBUG=true  # Linux/macOS
set DEBUG=true     # Windows

# Run with verbose output
python main.py --verbose
```

#### System Information
```bash
# Collect system info
python -c "
import sys, platform
print(f'Python: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Architecture: {platform.architecture()}')
"
```

## 📋 Post-Installation

### Configuration
```bash
# Copy example configuration
cp config.example.json config.json

# Edit configuration
nano config.json  # Linux/macOS
notepad config.json  # Windows
```

### First Run
```bash
# Desktop mode
python main.py

# API mode
python chatgpt_api_launcher.py
```

### Updates
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests
python test/test_imports.py
```

## 🎯 Next Steps

After successful installation:

1. **Read the Quick Start Guide**: `wiki/03-quick-start.md`
2. **Explore Examples**: `wiki/16-examples.md`
3. **Check API Documentation**: `http://localhost:8008/docs`
4. **Join Community**: GitHub Discussions
5. **Report Issues**: GitHub Issues

## 📞 Support

If you encounter issues during installation:

- **Check FAQ**: `wiki/15-faq.md`
- **Troubleshooting Guide**: `wiki/14-troubleshooting.md`
- **GitHub Issues**: Report installation problems
- **Community**: Ask for help in discussions
