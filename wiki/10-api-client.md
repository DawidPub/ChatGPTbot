# 💻 API Client

## 🎯 Przegląd

API Client to graficzny interfejs użytkownika do komunikacji z ChatGPT Bot API Server. Zapewnia wszystkie funkcjonalności aplikacji desktop, ale działa w architekturze klient-serwer.

## 🚀 Uruchomienie

### Metoda 1: Python Script
```bash
python chatgpt_api_client.py
```

### Metoda 2: Makefile
```bash
make client
```

### Metoda 3: API Launcher
```bash
python chatgpt_api_launcher.py
# Następnie kliknij "Start Client"
```

## 🏗️ Architektura

### HTTP Client Integration
```python
import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
import threading

class ChatGPTAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
        self.session = requests.Session()
        self.setup_gui()
```

### Connection Management
```python
def test_connection(self):
    """Testuje połączenie z serwerem API"""
    try:
        response = self.session.get(f"{self.base_url}/health", timeout=5)
        if response.status_code == 200:
            self.update_status("✅ Connected to API server")
            self.connection_status.config(text="Connected", fg="green")
            return True
        else:
            self.update_status("❌ API server returned error")
            self.connection_status.config(text="Error", fg="red")
            return False
    except requests.exceptions.RequestException as e:
        self.update_status(f"❌ Connection failed: {str(e)}")
        self.connection_status.config(text="Disconnected", fg="red")
        return False
```

## 🎨 Interfejs Użytkownika

### Main Window Layout
```
┌─────────────────────────────────────────────────────────┐
│ ChatGPT Bot - API Client                                │
├─────────────────────────────────────────────────────────┤
│ Server: [http://localhost:8000] [Test] Status: Connected│
├─────────────────────────────────────────────────────────┤
│ Session: [session-123] [New] [Delete] [Refresh]        │
├─────────────────────────────────────────────────────────┤
│ [Launch Browser] [Load State] [Save State] [Close]     │
├─────────────────────────────────────────────────────────┤
│ Question: ___________________________________________   │
│ [Ask Question]                                          │
├─────────────────────────────────────────────────────────┤
│ Response:                                               │
│ ┌─────────────────────────────────────────────────────┐ │
│ │                                                     │ │
│ │     API Response Area                               │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Status: Ready                                           │
└─────────────────────────────────────────────────────────┘
```

### GUI Components

#### Connection Panel
```python
def setup_connection_panel(self):
    """Konfiguruje panel połączenia"""
    conn_frame = ttk.LabelFrame(self.root, text="Server Connection")
    conn_frame.pack(fill="x", padx=5, pady=5)
    
    # Server URL
    ttk.Label(conn_frame, text="Server URL:").grid(row=0, column=0, sticky="w")
    self.server_url_var = tk.StringVar(value=self.base_url)
    self.server_url_entry = ttk.Entry(conn_frame, textvariable=self.server_url_var, width=40)
    self.server_url_entry.grid(row=0, column=1, padx=5)
    
    # Test connection button
    self.test_button = ttk.Button(conn_frame, text="Test Connection", 
                                 command=self.on_test_connection)
    self.test_button.grid(row=0, column=2, padx=5