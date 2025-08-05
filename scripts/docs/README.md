# 🚀 ChatGPT Bot API System

API system for remote control of ChatGPT Bot with web API functionality and a GUI client.

## 📋 Table of Contents

- [🎯 Features](#-features)
- [📦 Installation](#-installation)
- [🚀 Quick Start](#-quick-start)
- [🔧 System Components](#-system-components)
- [📖 API Endpoints](#-api-endpoints)
- [💻 Usage Examples](#-usage-examples)
- [🛠️ Troubleshooting](#️-troubleshooting)

## 🎯 Features

### 🖥️ API Server (FastAPI)
- **Session Management** - Creating, Monitoring, and Deleting Bot Sessions
- **Browser Control** - Launching, Saving/Loading State
- **Asking Questions** - Communicating with ChatGPT via API
- **Real-time Monitoring** - Session Logs and Status
- **Automatic Documentation** - Swagger UI under `/docs`

### 💻 API Client GUI
- **Graphical Interface** - Easy-to-use GUI similar to the original ChatGPTGUI
- **API Connection** - HTTP Communication with the Server
- **Auto-Refresh** - Automatically Refresh Status and Responses
- **Session Management** - Create and Cleanup Sessions
- **Response Logging** - Automatically Save to File

### 🎛️ Launcher GUI
- **Central Management** - Launch the Server and Client from One Location
- **Dependency Installation** - Automatically Install Required Packages
- **Process Monitoring** - Track Server and Client Status
- **Real-time Logs** - View Logs from Both Components

## 📦 Installation

### 1. Basic Requirements
Make sure you have installed:
- Python 3.7+
- All dependencies from the original ChatGPT Bot (selenium, webdriver-manager)

### 2. Installing API Dependencies
```bash
# Automatic installation via script

install_api_dependencies.bat

# Or manual installation

pip install fastapi uvicorn pydantic requests
```

### 3. Verifying the installation
```bash
python test_api.py
```

## 🚀 Quick Start

### Option 1: GUI Launcher (Recommended)
```bash
# Run the main launcher
RUN_ChatGPT_API.bat

# Or directly
python chatgpt_api_launcher.py
```

### Option 2: Manually launch
```bash
# Terminal 1: Start the API server
python chatgpt_api_server.py

# Terminal 2: Start the client (after starting the server)
python chatgpt_api_client.py
```

### Option 3: Batch Menu
```bash
# Start the interactive menu
RUN_ChatGPT_API.bat
```

## 🔧 System Components

### `chatgpt_api_server.py` - FastAPI Server
- **Port**: 8000 (default)
- **Documentation**: http://localhost:8000/docs
- **Features**: Bot Management, Sessions, API Endpoints

### `chatgpt_api_client.py` - GUI Client
- **Type**: Tkinter Application
- **Connection**: HTTP to API Server
- **Features**: GUI similar to ChatGPTGUI, but via API

### `chatgpt_api_launcher.py` - Launcher
- **Type**: System management GUI
- **Features**: Start/stop server and client, install DEP, monitoring

### `test_api.py` - Tests
- **Type**: Test script
- **Features**: Verify API functionality

## 📖 API Endpoints

### 🔗 Basic
- `GET /` - API information
- `GET /bot/sessions` - List all sessions

### 🤖 Bot Management
- `POST /bot/create` - Create a new bot session
- `DELETE /bot/{session_id}` - Delete a bot session

### 🌐 Browser Control
- `POST /bot/launch` - Launch browser
- `POST /bot/load_state` - Load browser state
- `POST /bot/save_state` - Save browser state
- `POST /bot/close` - Close browser

### ❓ Questions and Answers
- `POST /bot/ask` - Ask a ChatGPT question
- `GET /bot/status/{session_id}` - Get session status and logs

### 📊 API Usage Example

```python
import requests

# Create a session
response = requests.post("http://localhost:8000/bot/create")
session_id = response.json()["session_id"]

# Launch browser
requests.post("http://localhost:8000/bot/launch",

json={"session_id": session_id})

# Ask a question
requests.post("http://localhost:8000/bot/ask",

json={"session_id": session_id, "question": "What is AI?"})

# Check status
status = requests.get(f"http://localhost:8000/bot/status/{session_id}")
print(status.json())
```

## 💻 Usage examples

### 🎯 Scenario 1: Basic GUI usage
1. Run `chatgpt_api_launcher.py`
2. Click "Start Both (Server + Client)"
3. In the client, click "Connect & Create Session"
4. Click "Launch Browser"
5. Enter a question and click "Ask Question"

### 🎯 Scenario 2: Programmatic usage API
```python
from chatgpt_api_client import ChatGPTAPIClient

# Create a client
client = ChatGPTAPIClient("http://localhost:8000")

# Connect and create a session programmatically
# (requires modifying the class for programmatic use)
```

### 🎯 Scenario 3: Bulk processing
```python
import requests
import time

api_base = "http://localhost:8000"
questions = ["What is AI?", "Explain Python", "How does ML work?"]

# Create a session
session = requests.post(f"{api_base}/bot/create").json()
session_id = session["session_id"]

# Launch the browser
requests.post(f"{api_base}/bot/launch", json = {"session_id"})

