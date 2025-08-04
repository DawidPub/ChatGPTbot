# 🚀 Quick Start Guide

## 🎯 Overview

This guide will help you get ChatGPT Bot up and running in under 5 minutes. Choose your preferred mode and follow the steps below.

## 🖥️ Desktop Application (Easiest)

### Step 1: Launch the Application
```bash
# Method 1: Direct Python execution
python main.py

# Method 2: Using Makefile
make run-bot

# Method 3: Windows batch file
RUN_ChatGPT_Bot_WORKING.bat

# Method 4: Compiled executable
Final_Executables/ChatGPT_Bot_WORKING/ChatGPT_Bot_Working.exe
```

### Step 2: Start Browser
1. Click **"Launch Browser"** button
2. Wait for Chrome to open and navigate to ChatGPT
3. **Manual step**: Log in to your ChatGPT account if needed
4. Status should show "Browser launched successfully"

### Step 3: Ask Your First Question
1. Type your question in the text field
2. Click **"Ask Question"** or press Enter
3. Wait for the response to appear
4. The conversation will be displayed in the response area

### Step 4: Save Your Session (Optional)
1. Click **"Save State"** to preserve your login session
2. Next time, click **"Load State"** to restore your session
3. This avoids having to log in again

## 🌐 API System (Advanced)

### Step 1: Start the API System
```bash
# Method 1: API Launcher (Recommended)
python chatgpt_api_launcher.py

# Method 2: Manual server start
python chatgpt_api_server.py

# Method 3: Using Makefile
make run-api

# Method 4: Docker
docker-compose up -d
```

### Step 2: Access API Documentation
Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Step 3: Test API with curl
```bash
# Launch browser
curl -X POST "http://localhost:8000/bot/launch" \
     -H "Content-Type: application/json" \
     -d '{"headless": false}'

# Ask a question (replace SESSION_ID with actual ID from launch response)
curl -X POST "http://localhost:8000/bot/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Hello, ChatGPT!", "session_id": "SESSION_ID"}'
```

### Step 4: Use API Client GUI
```bash
# Start API client
python chatgpt_api_client.py

# Or use the launcher
python chatgpt_api_launcher.py
# Then click "Start Client"
```

## 🐳 Docker Quick Start

### Step 1: Start with Docker Compose
```bash
# Clone repository
git clone https://github.com/your-repo/chatgpt-bot.git
cd chatgpt-bot

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### Step 2: Verify Installation
```bash
# Check API health
curl http://localhost:8000/health

# View logs
docker-compose logs -f
```

### Step 3: Use the API
```bash
# Launch browser in container
curl -X POST "http://localhost:8000/bot/launch" \
     -H "Content-Type: application/json" \
     -d '{"headless": true}'
```

## 📱 First-Time Setup

### 1. ChatGPT Account
- Ensure you have a ChatGPT account at https://chat.openai.com
- Consider using ChatGPT Plus for better performance
- Have your login credentials ready

### 2. Browser Configuration
```python
# Default Chrome options (automatically applied)
--no-sandbox
--disable-dev-shm-usage
--disable-gpu
--window-size=1920,1080
```

### 3. Session Management
```bash
# Files created automatically:
chatgpt_cookies.pkl     # Login session cookies
chatgpt_session.json    # Browser session data
chatgpt_answer.txt      # Last response (desktop mode)
```

## 🎮 Basic Usage Examples

### Desktop Mode Example
```python
# This happens automatically when you use the GUI
from chatgpt_bot_core import ChatGPTBot

bot = ChatGPTBot()
bot.launch_browser(headless=False)
response = bot.ask_question_and_get_response("What is artificial intelligence?")
print(response)
bot.close_browser()
```

### API Mode Example
```python
import requests

# Launch browser
response = requests.post('http://localhost:8000/bot/launch', 
                        json={'headless': False})
session_id = response.json()['data']['session_id']

# Ask question
response = requests.post('http://localhost:8000/bot/ask', 
                        json={
                            'question': 'Explain quantum computing',
                            'session_id': session_id
                        })
print(response.json()['data']['answer'])
```

### JavaScript Example
```javascript
// Launch browser
const launchResponse = await fetch('http://localhost:8000/bot/launch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ headless: false })
});
const { session_id } = (await launchResponse.json()).data;

// Ask question
const askResponse = await fetch('http://localhost:8000/bot/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        question: 'Write a Python function to calculate fibonacci',
        session_id: session_id
    })
});
const result = await askResponse.json();
console.log(result.data.answer);
```

## 🔧 Configuration Options

### Environment Variables
```bash
# API Configuration
export API_HOST=localhost
export API_PORT=8000
export DEBUG=false

# Browser Configuration
export HEADLESS_DEFAULT=false
export BROWSER_TIMEOUT=30

# Session Configuration
export MAX_SESSIONS=10
export SESSION_TIMEOUT=3600
```

### Configuration File (config.json)
```json
{
    "browser": {
        "headless": false,
        "timeout": 30,
        "window_size": [1920, 1080],
        "user_data_dir": null
    },
    "api": {
        "host": "localhost",
        "port": 8000,
        "debug": false,
        "max_sessions": 10
    },
    "logging": {
        "level": "INFO",
        "file": "chatgpt_bot.log"
    }
}
```

## 🚨 Common First-Time Issues

### Issue 1: Chrome Not Found
```bash
# Solution: Install Chrome or Chromium
# Windows: Download from google.com/chrome
# Linux: sudo apt install google-chrome-stable
# macOS: brew install --cask google-chrome
```

### Issue 2: Permission Denied (Linux/macOS)
```bash
# Solution: Fix permissions
chmod +x *.sh
sudo chown -R $USER:$USER .
```

### Issue 3: Port Already in Use
```bash
# Solution: Change port or kill existing process
# Change port:
export API_PORT=8001
python chatgpt_api_server.py

# Or kill existing process:
lsof -ti:8000 | xargs kill -9  # Linux/macOS
netstat -ano | findstr :8000   # Windows (find PID and kill)
```

### Issue 4: ChatGPT Login Required
```
# This is normal! You need to:
1. Wait for browser to open
2. Log in to ChatGPT manually
3. Click "Save State" to remember login
4. Next time use "Load State" to skip login
```

## 📊 Performance Tips

### Desktop Mode
- Use headless mode for better performance: `headless=True`
- Save state frequently to avoid re-login
- Close browser when done to free memory

### API Mode
- Use session management for multiple concurrent users
- Enable headless mode for production: `{"headless": true}`
- Monitor memory usage with multiple sessions

### Docker Mode
- Allocate sufficient memory: `--memory=2g`
- Use shared memory: `--shm-size=2g`
- Monitor container resources: `docker stats`

## 🎯 Next Steps

After completing the quick start:

1. **Explore Advanced Features**: Check `wiki/05-system-components.md`
2. **API Integration**: Read `wiki/06-api-reference.md`
3. **Docker Deployment**: See `wiki/09-docker.md`
4. **Development**: Review `wiki/11-development.md`
5. **Examples**: Browse `wiki/16-examples.md`

## 🆘 Getting Help

If you encounter issues:

1. **Check Status**: Look at the status bar/logs for error messages
2. **Verify Installation**: Run `python test/test_imports.py`
3. **Check Dependencies**: Ensure Chrome and Python are properly installed
4. **Read FAQ**: Common solutions in `wiki/15-faq.md`
5. **Report Issues**: Create a GitHub issue with error details

## 🎉 Success Indicators

You know everything is working when:

- ✅ Browser launches without errors
- ✅ ChatGPT interface loads properly
- ✅ Questions receive responses
- ✅ API endpoints return successful responses
- ✅ No error messages in logs/status

## 📞 Support Channels

- **Documentation**: Complete wiki in `/wiki` folder
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community help and questions
- **Email**: Direct contact with maintainers

Happy automating! 🤖✨
