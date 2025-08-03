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
requests.post(f"{api_base}/bot/launch", json = {"session_id"

⭐⭐⭐ A gift for ignoramuses who don't know English ;-) ⭐⭐⭐

# 🚀 ChatGPT Bot API System

System API do zdalnego sterowania ChatGPT Bot z funkcjonalnością web API i klientem GUI.

## 📋 Spis treści

- [🎯 Funkcjonalności](#-funkcjonalności)
- [📦 Instalacja](#-instalacja)
- [🚀 Szybki start](#-szybki-start)
- [🔧 Składniki systemu](#-składniki-systemu)
- [📖 API Endpoints](#-api-endpoints)
- [💻 Przykłady użycia](#-przykłady-użycia)
- [🛠️ Rozwiązywanie problemów](#️-rozwiązywanie-problemów)

## 🎯 Funkcjonalności

### 🖥️ Serwer API (FastAPI)
- **Zarządzanie sesjami** - Tworzenie, monitorowanie i usuwanie sesji botów
- **Sterowanie przeglądarką** - Uruchamianie, zapisywanie/ładowanie stanu
- **Zadawanie pytań** - Komunikacja z ChatGPT przez API
- **Monitoring w czasie rzeczywistym** - Logi i statusy sesji
- **Automatyczna dokumentacja** - Swagger UI pod `/docs`

### 💻 Klient API GUI
- **Interfejs graficzny** - Łatwe w użyciu GUI podobne do oryginalnego ChatGPTGUI
- **Połączenie API** - Komunikacja przez HTTP z serwerem
- **Auto-refresh** - Automatyczne odświeżanie statusu i odpowiedzi
- **Zarządzanie sesjami** - Tworzenie i cleanup sesji
- **Zapis odpowiedzi** - Automatyczny zapis do pliku

### 🎛️ Launcher GUI
- **Centralne zarządzanie** - Uruchamianie serwera i klienta z jednego miejsca
- **Instalacja dependencies** - Automatyczna instalacja wymaganych pakietów
- **Monitoring procesów** - Śledzenie statusu serwera i klienta
- **Logi w czasie rzeczywistym** - Podgląd logów z obu komponentów

## 📦 Instalacja

### 1. Wymagania podstawowe
Upewnij się, że masz zainstalowane:
- Python 3.7+
- Wszystkie zależności z oryginalnego ChatGPT Bot (selenium, webdriver-manager)

### 2. Instalacja zależności API
```bash
# Automatyczna instalacja przez skrypt
install_api_dependencies.bat

# Lub ręczna instalacja
pip install fastapi uvicorn pydantic requests
```

### 3. Weryfikacja instalacji
```bash
python test_api.py
```

## 🚀 Szybki start

### Opcja 1: Launcher GUI (Rekomendowane)
```bash
# Uruchom główny launcher
RUN_ChatGPT_API.bat

# Lub bezpośrednio
python chatgpt_api_launcher.py
```

### Opcja 2: Ręczne uruchomienie
```bash
# Terminal 1: Uruchom serwer API
python chatgpt_api_server.py

# Terminal 2: Uruchom klienta (po uruchomieniu serwera)
python chatgpt_api_client.py
```

### Opcja 3: Menu wsadowe
```bash
# Uruchom interaktywne menu
RUN_ChatGPT_API.bat
```

## 🔧 Składniki systemu

### `chatgpt_api_server.py` - Serwer FastAPI
- **Port**: 8000 (domyślnie)
- **Dokumentacja**: http://localhost:8000/docs
- **Funkcje**: Zarządzanie botami, sesje, API endpoints

### `chatgpt_api_client.py` - Klient GUI
- **Typ**: Aplikacja tkinter
- **Połączenie**: HTTP do serwera API
- **Funkcje**: GUI podobne do ChatGPTGUI, ale przez API

### `chatgpt_api_launcher.py` - Launcher
- **Typ**: GUI do zarządzania systemem
- **Funkcje**: Start/stop serwera i klienta, instalacja deps, monitoring

### `test_api.py` - Testy
- **Typ**: Skrypt testowy
- **Funkcje**: Weryfikacja działania API

## 📖 API Endpoints

### 🔗 Podstawowe
- `GET /` - Informacje o API
- `GET /bot/sessions` - Lista wszystkich sesji

### 🤖 Zarządzanie botami
- `POST /bot/create` - Utwórz nową sesję bota
- `DELETE /bot/{session_id}` - Usuń sesję bota

### 🌐 Sterowanie przeglądarką
- `POST /bot/launch` - Uruchom przeglądarkę
- `POST /bot/load_state` - Załaduj stan przeglądarki
- `POST /bot/save_state` - Zapisz stan przeglądarki
- `POST /bot/close` - Zamknij przeglądarkę

### ❓ Pytania i odpowiedzi
- `POST /bot/ask` - Zadaj pytanie ChatGPT
- `GET /bot/status/{session_id}` - Pobierz status i logi sesji

### 📊 Przykład użycia API

```python
import requests

# Utwórz sesję
response = requests.post("http://localhost:8000/bot/create")
session_id = response.json()["session_id"]

# Uruchom przeglądarkę
requests.post("http://localhost:8000/bot/launch", 
              json={"session_id": session_id})

# Zadaj pytanie
requests.post("http://localhost:8000/bot/ask", 
              json={"session_id": session_id, "question": "What is AI?"})

# Sprawdź status
status = requests.get(f"http://localhost:8000/bot/status/{session_id}")
print(status.json())
```

## 💻 Przykłady użycia

### 🎯 Scenariusz 1: Podstawowe użycie przez GUI
1. Uruchom `chatgpt_api_launcher.py`
2. Kliknij "Start Both (Server + Client)"
3. W kliencie kliknij "Connect & Create Session"
4. Kliknij "Launch Browser"
5. Wpisz pytanie i kliknij "Ask Question"

### 🎯 Scenariusz 2: Programowe użycie API
```python
from chatgpt_api_client import ChatGPTAPIClient

# Utwórz klienta
client = ChatGPTAPIClient("http://localhost:8000")

# Połącz i utwórz sesję programowo
# (wymaga modyfikacji klasy dla programowego użycia)
```

### 🎯 Scenariusz 3: Bulk processing
```python
import requests
import time

api_base = "http://localhost:8000"
questions = ["What is AI?", "Explain Python", "How does ML work?"]

# Utwórz sesję
session = requests.post(f"{api_base}/bot/create").json()
session_id = session["session_id"]

# Uruchom przeglądarkę
requests.post(f"{api_base}/bot/launch", json={"session_id": session_id})

# Zadaj wszystkie pytania
for i, question in enumerate(questions):
    print(f"Asking question {i+1}: {question}")
    requests.post(f"{api_base}/bot/ask", 
                  json={"session_id": session_id, "question": question})
    
    # Czekaj na odpowiedź
    while True:
        status = requests.get(f"{api_base}/bot/status/{session_id}").json()
        if status.get("current_response"):
            print(f"Answer {i+1}: {status['current_response'][:100]}...")
            break
        time.sleep(2)
```

## 🛠️ Rozwiązywanie problemów

### ❌ "Cannot connect to API server"
```bash
# Sprawdź czy serwer działa
curl http://localhost:8000/

# Lub uruchom serwer
python chatgpt_api_server.py
```

### ❌ "Import fastapi could not be resolved"
```bash
# Zainstaluj dependencies
pip install fastapi uvicorn pydantic requests

# Lub użyj skryptu
install_api_dependencies.bat
```

### ❌ Serwer nie odpowiada
```bash
# Sprawdź port
netstat -an | findstr :8000

# Sprawdź czy inny proces używa portu
tasklist | findstr python
```

### ❌ Klient nie łączy się z serwerem
1. Sprawdź czy serwer działa: http://localhost:8000/
2. Sprawdź URL w kliencie (domyślnie http://localhost:8000)
3. Sprawdź firewall/antywirus

### ❌ Brak odpowiedzi na pytania
1. Sprawdź czy przeglądarka została uruchomiona
2. Sprawdź czy jesteś zalogowany do ChatGPT
3. Sprawdź logi w `/bot/status/{session_id}`

## 📁 Struktura plików

```
chatgpt_api_server.py      # 🖥️ Serwer FastAPI
chatgpt_api_client.py      # 💻 Klient GUI
chatgpt_api_launcher.py    # 🎛️ Launcher GUI
test_api.py                # 🧪 Testy API
install_api_dependencies.bat # 📦 Instalator deps
RUN_ChatGPT_API.bat       # 🚀 Główny launcher
README_API.md             # 📖 Ta dokumentacja

# Oryginalne pliki
chatgpt_gui.py            # 🖥️ Oryginalny GUI (lokalne użycie)
chatgpt_bot_core.py       # 🤖 Logika bota
main.py                   # 🚀 Główny punkt wejścia
```

## 🎉 Korzyści API

### 🌐 Rozdzielenie odpowiedzialności
- **Serwer**: Zarządza botami i przeglądarkami
- **Klient**: Interfejs użytkownika
- **API**: Komunikacja między komponentami

### 🔄 Skalowalność
- Wielu klientów może łączyć się z jednym serwerem
- Możliwość uruchomienia na różnych maszynach  
- Łatwe dodawanie nowych klientów (web, mobile, CLI)

### 🛡️ Bezpieczeństwo
- Centralne zarządzanie sesjami
- Możliwość dodania autoryzacji
- Izolacja procesów przeglądarki

### 🚀 Elastyczność
- RESTful API - łatwa integracja
- Dokumentacja Swagger
- Możliwość użycia z innych języków programowania

---

**🎯 Gotowe do użycia!** Uruchom `RUN_ChatGPT_API.bat` i wybierz opcję 2 dla pełnego doświadczenia GUI! 🚀
