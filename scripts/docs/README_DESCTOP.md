# ChatGPT Bot - Complete Solution
This is a ChatGPT Bot project - a Python automation tool that provides multiple ways to interact with ChatGPT through web automation using Selenium.

🎯 Core Features
Web automation for ChatGPT using Selenium WebDriver
GUI interface built with Tkinter for easy interaction
Session management - save/load browser state and cookies
Multiple deployment options - Desktop app, API server, or Docker

🚀 Available Modes

🖥️ Desktop Application - Traditional GUI (`main.py`, `chatgpt_gui.py`)

📱 API Server - FastAPI-based server with REST endpoints (`chatgpt_api_server.py`)

🐳 Docker - Containerized deployment with VNC access

💻 API Client - GUI client that connects to the API server

🛠️ Key Components
`chatgpt_bot_core.py` - Core automation logic
`chatgpt_gui.py` - Desktop GUI interface
`chatgpt_api_server.py` - FastAPI server
`chatgpt_api_client.py` - API client GUI
Cross-platform support (Windows `.bat` + Linux `.sh` scripts)

📦 Tech Stack
Selenium + webdriver-manager for browser automation
Tkinter for desktop GUI
FastAPI + Uvicorn for API server
Docker for containerization
PyInstaller for executable compilation
The project offers flexibility from simple desktop use to scalable API-based deployments.

## 🚀 Available Startup Modes

### 1. 🐳 Docker (Recommended)
```batch
# Windows
start-docker.bat

# Linux/macOS
./start-docker.sh
```

### 2. 📱 API Server
```batch
# Windows
RUN_ChatGPT_API.bat

# Linux/macOS
./run_chatgpt_api.sh
```

### 3. 🖥️ Desktop Application
```batch
# Windows
RUN_ChatGPT_working.bat

# Linux/macOS
./run_chatgpt_bot_working.sh
```

## 🐳 Docker - The Easiest Way

### Quick Start
1. Install Docker Desktop
2. Run: `start-docker.bat` (Windows) or `./start-docker.sh` (Linux)
3. Open: http://localhost:8008

### Accessing the GUI via VNC
- Address: localhost:5900
- Password: none
- VNC client: TightVNC, RealVNC, or UltraVNC

More information: [README-Windows.md](README-Windows.md) | [INSTALL_LINUX.md](INSTALL_LINUX.md)


## Prerequisites
- Python 3.7 or higher installed
- Internet connection for downloading packages

## Compilation Steps

1. **Install Dependencies**
   - Run `pip install -r requirements.txt` to install required packages

2. **Compile to Executable**
   - Option A: Run `compile.bat` (recommended)
   - Option B: Run `pyinstaller chatgpt_bot.spec` manually

3. **Find Your Executable**
   - The compiled executable will be in the `dist/` folder
   - File name: `ChatGPT_Bot.exe`

## Running the Executable

1. Navigate to the `dist/` folder
2. Double-click `ChatGPT_Bot.exe`
3. The GUI will open with the ChatGPT Bot interface

## Features

- **Launch Browser**: Opens Chrome browser for ChatGPT
- **Load Browser State**: Restores saved session and cookies
- **Save Browser State**: Saves current session for future use
- **Ask Question**: Send questions to ChatGPT and get responses
- **Close Browser**: Safely closes the browser

## Files Created

- `chatgpt_cookies.pkl`: Saved browser cookies
- `chatgpt_session.json`: Saved session data
- `chatgpt_answer.txt`: Latest ChatGPT response

## Troubleshooting

1. **Chrome not found**: Make sure Chrome is installed
2. **Selenium errors**: The webdriver will be downloaded automatically
3. **Permission errors**: Run as administrator if needed
4. **Antivirus warnings**: The executable is safe - add exception if needed

## Distribution

The `ChatGPT_Bot.exe` file is self-contained and can be shared/moved to other Windows computers without requiring Python installation.
