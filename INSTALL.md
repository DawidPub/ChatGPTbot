# 📦 ChatGPT Bot - Dependencies Installation

## 🚀 Fast installation of all packages

```bash
# Install all packages from requirements.txt
pip install -r requirements.txt
```

## 🔧 Step-by-step installation

### 1. Core packages (required)
```bash
pip install selenium>=4.0.0 webdriver-manager>=3.8.0
```

### 2. API packages (for the API system)
```bash
pip install fastapi>=0.100.0 uvicorn>=0.20.0 pydantic>=2.0.0 requests>=2.28.0
```

### 3. Development tools (optional)
```bash
pip install pyinstaller>=6.0.0 pytest>=7.0.0 black>=22.0.0 flake8>=4.0.0
```

### 4. Additional utilities (optional)
```bash
pip install python-multipart>=0.0.5 aiofiles>=0.8.0
```

## 🎯 Environment-specific versions

### Python 3.12.7 (as in your environment)
```bash
# Use specific Python
"C:\Program Files\Python312\python.exe" -m pip install -r requirements.txt
```

### For a virtual environment
```bash
# Activate venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🔍 Verifying installation

### Check installed packages
```bash
pip list | findstr -i "selenium fastapi uvicorn pydantic requests"
```

### Test imports
```python
# test_imports.py
try:
import selenium
import webdriver_manager
import fastapi
import uvicorn
import pydantic
import requests
print("✅ All packages installed successfully!")
except ImportError as e:
print(f"❌ Import error: {e}")
```

## 🚀 Automated scripts

### Windows
```batch
REM Use install_api_dependencies.bat
install_api_dependencies.bat
```

### Or via the launcher
```batch
REM Run the launcher and select option 1
RUN_ChatGPT_API.bat
```

## 🛠️ Troubleshooting

### "Command not found: pip" error
```bash
python -m pip install -r requirements.txt
```

### Permission errors
```bash
pip install --user -r requirements.txt
```

### Version conflicts
```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

### Checking the Python version
```bash
python --version
pip --version
```

## 📋 List of all dependencies

| Package | Version | Description |
|--------|--------|------|
| selenium | >=4.0.0 | WebDriver for browser automation |
| webdriver-manager | >=3.8.0 | Automatic driver management |
| fastapi | >=0.100.0 | API Framework |
| uvicorn | >=0.20.0 | ASGI Server |
| pydantic | >=2.0.0 | Data Validation |
| requests | >=2.28.0 | HTTP Client |
| pyinstaller | >=6.0.0 | Compiling to Executable |
| pytest | >=7.0.0 | Test Framework |
| black | >=22.0.0 | Code Formatting |
| flake8 | >=4.0.0 | Linting |
| python-multipart | >=0.0.5 | Form Handling |
| aiofiles | >=0.8.0 | Async I/O |

--
**💡 Tip:** Use `RUN_ChatGPT_API.bat` → option 1 for automatic installation! 🚀


⭐⭐⭐ A gift for ignoramuses who don't know English ;-) ⭐⭐⭐


# 📦 ChatGPT Bot - Instalacja Dependencies

## 🚀 Szybka instalacja wszystkich pakietów

```bash
# Instaluj wszystkie pakiety z requirements.txt
pip install -r requirements.txt
```

## 🔧 Instalacja krokowa

### 1. Podstawowe pakiety (wymagane)
```bash
pip install selenium>=4.0.0 webdriver-manager>=3.8.0
```

### 2. Pakiety API (dla systemu API)
```bash
pip install fastapi>=0.100.0 uvicorn>=0.20.0 pydantic>=2.0.0 requests>=2.28.0
```

### 3. Narzędzia deweloperskie (opcjonalne)
```bash
pip install pyinstaller>=6.0.0 pytest>=7.0.0 black>=22.0.0 flake8>=4.0.0
```

### 4. Dodatkowe utilities (opcjonalne)
```bash
pip install python-multipart>=0.0.5 aiofiles>=0.8.0
```

## 🎯 Wersje specyficzne dla środowiska

### Python 3.12.7 (jak w Twoim środowisku)
```bash
# Użyj specifycznego Python
"C:\Program Files\Python312\python.exe" -m pip install -r requirements.txt
```

### Dla środowiska wirtualnego
```bash
# Aktywuj venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🔍 Weryfikacja instalacji

### Sprawdź zainstalowane pakiety
```bash
pip list | findstr -i "selenium fastapi uvicorn pydantic requests"
```

### Test importów
```python
# test_imports.py
try:
    import selenium
    import webdriver_manager
    import fastapi
    import uvicorn
    import pydantic
    import requests
    print("✅ Wszystkie pakiety zainstalowane poprawnie!")
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
```

## 🚀 Skrypty automatyczne

### Windows
```batch
REM Użyj install_api_dependencies.bat
install_api_dependencies.bat
```

### Lub przez launcher
```batch
REM Uruchom launcher i wybierz opcję 1
RUN_ChatGPT_API.bat
```

## 🛠️ Rozwiązywanie problemów

### Błąd "command not found: pip"
```bash
python -m pip install -r requirements.txt
```

### Błędy uprawnień
```bash
pip install --user -r requirements.txt
```

### Konflikty wersji
```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

### Sprawdzenie wersji Python
```bash
python --version
pip --version
```

## 📋 Lista wszystkich dependencies

| Pakiet | Wersja | Opis |
|--------|--------|------|
| selenium | >=4.0.0 | WebDriver dla automatyzacji przeglądarki |
| webdriver-manager | >=3.8.0 | Automatyczne zarządzanie sterownikami |
| fastapi | >=0.100.0 | Framework API |
| uvicorn | >=0.20.0 | Serwer ASGI |
| pydantic | >=2.0.0 | Walidacja danych |
| requests | >=2.28.0 | Klient HTTP |
| pyinstaller | >=6.0.0 | Kompilacja do executable |
| pytest | >=7.0.0 | Framework testowy |
| black | >=22.0.0 | Formatowanie kodu |
| flake8 | >=4.0.0 | Linting |
| python-multipart | >=0.0.5 | Obsługa formularzy |
| aiofiles | >=0.8.0 | Async I/O |

---
**💡 Tip:** Użyj `RUN_ChatGPT_API.bat` → opcja 1 dla automatycznej instalacji! 🚀
