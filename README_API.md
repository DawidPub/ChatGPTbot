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
