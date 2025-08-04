# 🐧 ChatGPT Bot - Linux Installation Guide

## 📋 Quick Start (Ubuntu/Debian)

```bash
# 1. Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# 2. Clone/download the project
# (assuming you already have the files)

# 3. Make scripts executable
chmod +x *.sh

# 4. Install all dependencies
./install_all_dependencies.sh

# 5. Run the system
./run_chatgpt_api.sh
```

## 🎯 Distribution-Specific Instructions

### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv python3-tk

# Install Chrome (for selenium)
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable

# Install dependencies
./install_all_dependencies.sh
```

### CentOS/RHEL/Fedora
```bash
# CentOS/RHEL
sudo yum install python3 python3-pip python3-tkinter git

# Fedora
sudo dnf install python3 python3-pip python3-tkinter git

# Install Chrome
# CentOS/RHEL
sudo yum install -y wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum localinstall google-chrome-stable_current_x86_64.rpm

# Fedora
sudo dnf install google-chrome-stable

# Install dependencies
./install_all_dependencies.sh
```

### Arch Linux
```bash
# Install Python and pip
sudo pacman -S python python-pip python-tkinter git

# Install Chrome
yay -S google-chrome
# or
sudo pacman -S chromium

# Install dependencies
./install_all_dependencies.sh
```

### openSUSE
```bash
# Install Python and pip
sudo zypper install python3 python3-pip python3-tk git

# Install Chrome
sudo zypper ar http://dl.google.com/linux/chrome/rpm/stable/x86_64 Google-Chrome
sudo zypper ref
sudo zypper install google-chrome-stable

# Install dependencies
./install_all_dependencies.sh
```

## 🛠️ Alternative Installation Methods

### Method 1: Using Make
```bash
# Install make if not available
sudo apt install make  # Ubuntu/Debian
# sudo yum install make  # CentOS/RHEL
# sudo dnf install make  # Fedora

# Show available commands
make help

# Install dependencies
make install

# Run the system
make run-api
```

### Method 2: Using Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv chatgpt-bot-env

# Activate virtual environment
source chatgpt-bot-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the system
python chatgpt_api_server.py  # In one terminal
python chatgpt_api_client.py  # In another terminal
```

### Method 3: Using Docker
```bash
# Install Docker
sudo apt install docker.io docker-compose  # Ubuntu/Debian

# Build and run
docker-compose up --build

# Access API at http://localhost:8000
```

## 🔧 Troubleshooting

### Python Issues
```bash
# Check Python version
python3 --version

# If python3 not found, try:
ls /usr/bin/python*

# Install alternative Python version
sudo apt install python3.11 python3.11-pip
```

### Pip Issues
```bash
# Install pip if missing
curl https://bootstrap.pypa.io/get-pip.py | python3

# Upgrade pip
python3 -m pip install --upgrade pip

# Install to user directory (if permission issues)
python3 -m pip install --user -r requirements.txt
```

### Chrome/Chromium Issues
```bash
# Install Chromium as alternative
sudo apt install chromium-browser  # Ubuntu/Debian
sudo yum install chromium          # CentOS/RHEL
sudo dnf install chromium          # Fedora

# For headless servers (no GUI)
sudo apt install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

### Permission Issues
```bash
# Make scripts executable
chmod +x *.sh

# If still having issues
sudo chmod +x *.sh
```

### GUI Issues (tkinter)
```bash
# Install tkinter
sudo apt install python3-tk        # Ubuntu/Debian
sudo yum install tkinter           # CentOS/RHEL
sudo dnf install python3-tkinter   # Fedora

# For X11 forwarding over SSH
ssh -X username@hostname
```

## 📊 System Requirements

### Minimum Requirements
- **OS**: Any Linux distribution with Python 3.7+
- **RAM**: 2GB (4GB recommended)
- **Storage**: 1GB free space
- **Browser**: Chrome/Chromium
- **Network**: Internet connection

### Recommended Setup
- **OS**: Ubuntu 20.04+ or equivalent
- **RAM**: 4GB+
- **CPU**: 2+ cores
- **Storage**: 2GB+ free space
- **Browser**: Latest Chrome
- **Display**: GUI environment or X11 forwarding

## 🚀 Available Commands After Installation

### Quick Commands
```bash
# Check what's available
ls *.sh

# Main launcher (interactive menu)
./run_chatgpt_api.sh

# Quick bot launcher
./run_chatgpt_bot_working.sh

# Check dependencies
./check_dependencies.sh
```

### Make Commands (if available)
```bash
make help           # Show all commands
make install        # Install dependencies
make run-api        # Run API system
make run-bot        # Run original bot
make test           # Run tests
make clean          # Clean temporary files
```

### Direct Python Commands
```bash
# API Server
python3 chatgpt_api_server.py

# API Client
python3 chatgpt_api_client.py

# Original Bot
python3 main.py
# or
python3 chatgpt_gui.py

# Tests
python3 test_api.py
```

## 🌐 Network Configuration

### Firewall (if needed)
```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 8000/tcp

# CentOS/RHEL (firewalld)
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload

# iptables (generic)
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

### Access from Other Machines
Edit `chatgpt_api_server.py` and change:
```python
# From:
uvicorn.run(app, host="0.0.0.0", port=8000)

# To (for external access):
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 📁 File Permissions Reference

```bash
# Make all shell scripts executable
chmod +x *.sh

# Specific permissions
chmod 755 *.sh              # Read, write, execute for owner; read, execute for others
chmod 644 *.py              # Read, write for owner; read for others
chmod 644 requirements.txt  # Read, write for owner; read for others
```

## 🎉 Success Verification

After installation, verify everything works:

```bash
# 1. Check Python
python3 --version

# 2. Check dependencies
./check_dependencies.sh

# 3. Test API
python3 test_api.py

# 4. Run full system
./run_chatgpt_api.sh
```

---

**🎯 You're ready!** Your ChatGPT Bot system should now work perfectly on Linux! 🐧🚀
