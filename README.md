# ChatGPT Bot - Complete Solution

## 🚀 Dostępne tryby uruchomienia

### 1. 🐳 Docker (Zalecane)
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

## 🐳 Docker - Najłatwiejszy sposób

### Szybki start
1. Zainstaluj Docker Desktop
2. Uruchom: `start-docker.bat` (Windows) lub `./start-docker.sh` (Linux)
3. Otwórz: http://localhost:8000

### Dostęp do GUI przez VNC
- Adres: localhost:5900
- Hasło: brak
- Klient VNC: TightVNC, RealVNC, lub UltraVNC

Więcej informacji: [README-Windows.md](README-Windows.md) | [INSTALL_LINUX.md](INSTALL_LINUX.md)

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
