# 🖥️ Aplikacja Desktop

## 🎯 Przegląd

Aplikacja desktop to główny interfejs użytkownika dla ChatGPT Bot, zbudowany w Tkinter. Oferuje intuicyjny GUI do zarządzania przeglądarką i komunikacji z ChatGPT.

## 🚀 Uruchomienie

### Metoda 1: Python Script
```bash
python main.py
```

### Metoda 2: Skompilowany Executable
```bash
# Windows
Final_Executables/ChatGPT_Bot_WORKING/ChatGPT_Bot_Working.exe

# Linux/macOS
./Final_Executables/ChatGPT_Bot_WORKING/ChatGPT_Bot_Working
```

### Metoda 3: Makefile
```bash
make run-bot
```

## 🎨 Interfejs Użytkownika

### Główne Okno
```
┌─────────────────────────────────────────┐
│ ChatGPT Bot - Desktop Application      │
├─────────────────────────────────────────┤
│ [Launch Browser] [Load State] [Save]   │
│ [Close Browser]                         │
├─────────────────────────────────────────┤
│ Question: ___________________________   │
│ [Ask Question]                          │
├─────────────────────────────────────────┤
│ Response:                               │
│ ┌─────────────────────────────────────┐ │
│ │                                     │ │
│ │     ChatGPT Response Area           │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ Status: Ready                           │
└─────────────────────────────────────────┘
```

### Komponenty GUI

#### Control Panel
- **Launch Browser**: Uruchamia Chrome z ChatGPT
- **Load State**: Ładuje zapisane cookies i sesję
- **Save State**: Zapisuje aktualny stan przeglądarki
- **Close Browser**: Zamyka przeglądarkę

#### Question Section
- **Question Entry**: Pole tekstowe do wprowadzania pytań
- **Ask Question**: Wysyła pytanie do ChatGPT

#### Response Section
- **Response Text Area**: Scrollowalne pole z odpowiedziami
- **Auto-scroll**: Automatyczne przewijanie do najnowszej odpowiedzi

#### Status Bar
- **Status Label**: Informacje o aktualnym stanie aplikacji

## 🔧 Funkcjonalności

### Browser Management

#### Launch Browser
```python
def on_launch_browser(self):
    """Uruchamia przeglądarkę Chrome"""
    self.update_status("Launching browser...")
    
    # Opcje headless mode
    headless = self.headless_var.get()
    
    success = self.bot.launch_browser(headless=headless)
    if success:
        self.update_status("Browser launched successfully")
        self.enable_controls()
    else:
        self.update_status("Failed to launch browser")
```

#### State Management
```python
def on_load_state(self):
    """Ładuje zapisany stan sesji"""
    if self.bot.load_browser_state():
        self.update_status("Browser state loaded")
    else:
        self.update_status("Failed to load browser state")

def on_save_state(self):
    """Zapisuje aktualny stan sesji"""
    if self.bot.save_browser_state():
        self.update_status("Browser state saved")
    else:
        self.update_status("Failed to save browser state")
```

### Question & Response Handling

#### Ask Question
```python
def on_ask_question(self):
    """Wysyła pytanie do ChatGPT"""
    question = self.question_entry.get().strip()
    if not question:
        self.update_status("Please enter a question")
        return
    
    self.update_status("Asking question...")
    self.question_entry.config(state='disabled')
    self.ask_button.config(state='disabled')
    
    # Async call to prevent GUI freezing
    threading.Thread(target=self._ask_question_thread, 
                    args=(question,)).start()

def _ask_question_thread(self, question):
    """Thread worker dla pytań"""
    response = self.bot.ask_question_and_get_response(question)
    
    # Update GUI in main thread
    self.root.after(0, self._update_response, question, response)
```

#### Response Display
```python
def _update_response(self, question, response):
    """Aktualizuje wyświetlanie odpowiedzi"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Format response
    formatted_response = f"\n[{timestamp}] Q: {question}\n"
    formatted_response += f"A: {response}\n"
    formatted_response += "-" * 50 + "\n"
    
    # Update text area
    self.response_text.config(state='normal')
    self.response_text.insert(tk.END, formatted_response)
    self.response_text.config(state='disabled')
    self.response_text.see(tk.END)
    
    # Re-enable controls
    self.question_entry.config(state='normal')
    self.ask_button.config(state='normal')
    self.question_entry.delete(0, tk.END)
    self.question_entry.focus()
```

## ⚙️ Konfiguracja

### Window Settings
```python
class ChatGPTGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ChatGPT Bot - Desktop Application")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
```

### Theme & Styling
```python
def setup_styles(self):
    """Konfiguruje style GUI"""
    # Colors
    self.bg_color = "#f0f0f0"
    self.button_color = "#4CAF50"
    self.text_color = "#333333"
    
    # Fonts
    self.default_font = ("Arial", 10)
    self.button_font = ("Arial", 10, "bold")
    self.status_font = ("Arial", 9)
    
    # Apply to root
    self.root.configure(bg=self.bg_color)
```

### Keyboard Shortcuts
```python
def setup_bindings(self):
    """Konfiguruje skróty klawiszowe"""
    # Enter to ask question
    self.question_entry.bind('<Return>', 
                           lambda e: self.on_ask_question())
    
    # Ctrl+L to launch browser
    self.root.bind('<Control-l>', 
                  lambda e: self.on_launch_browser())
    
    # Ctrl+S to save state
    self.root.bind('<Control-s>', 
                  lambda e: self.on_save_state())
    
    # Ctrl+Q to quit
    self.root.bind('<Control-q>', 
                  lambda e: self.on_close())
```

## 🎛️ Advanced Features

### Settings Dialog
```python
def open_settings(self):
    """Otwiera okno ustawień"""
    settings_window = tk.Toplevel(self.root)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    
    # Headless mode checkbox
    tk.Checkbutton(settings_window, 
                  text="Headless Mode",
                  variable=self.headless_var).pack()
    
    # Timeout setting
    tk.Label(settings_window, text="Timeout (seconds):").pack()
    timeout_entry = tk.Entry(settings_window)
    timeout_entry.pack()
    timeout_entry.insert(0, str(self.timeout))
```

### History Management
```python
class ConversationHistory:
    def __init__(self):
        self.history = []
        self.max_history = 100
    
    def add_conversation(self, question, response):
        """Dodaje rozmowę do historii"""
        conversation = {
            'timestamp': datetime.now(),
            'question': question,
            'response': response
        }
        self.history.append(conversation)
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def save_to_file(self, filename="conversation_history.json"):
        """Zapisuje historię do pliku"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, default=str)
```

### Export Functions
```python
def export_conversation(self):
    """Eksportuje rozmowę do pliku"""
    from tkinter import filedialog
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), 
                  ("JSON files", "*.json"),
                  ("All files", "*.*")]
    )
    
    if filename:
        content = self.response_text.get(1.0, tk.END)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        self.update_status(f"Conversation exported to {filename}")
```

## 🔧 Error Handling

### GUI Error Display
```python
def show_error(self, title, message):
    """Wyświetla okno błędu"""
    from tkinter import messagebox
    messagebox.showerror(title, message)

def show_warning(self, title, message):
    """Wyświetla ostrzeżenie"""
    from tkinter import messagebox
    messagebox.showwarning(title, message)

def show_info(self, title, message):
    """Wyświetla informację"""
    from tkinter import messagebox
    messagebox.showinfo(title, message)
```

### Exception Handling
```python
def safe_execute(self, func, *args, **kwargs):
    """Bezpieczne wykonanie funkcji z obsługą błędów"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        self.update_status(error_msg)
        self.show_error("Operation Failed", error_msg)
        return None
```

## 📱 Responsive Design

### Window Resizing
```python
def configure_grid_weights(self):
    """Konfiguruje responsywność"""
    # Main window
    self.root.grid_rowconfigure(2, weight=1)  # Response area
    self.root.grid_columnconfigure(0, weight=1)
    
    # Response frame
    self.response_frame.grid_rowconfigure(1, weight=1)
    self.response_frame.grid_columnconfigure(0, weight=1)
```

### Dynamic Font Scaling
```python
def on_window_resize(self, event):
    """Dostosowuje rozmiar czcionki do okna"""
    width = event.width
    if width < 600:
        font_size = 8
    elif width < 800:
        font_size = 10
    else:
        font_size = 12
    
    self.update_font_size(font_size)
```

## 🎨 Customization

### Theme Support
```python
THEMES = {
    'light': {
        'bg': '#ffffff',
        'fg': '#000000',
        'button_bg': '#e0e0e0',
        'entry_bg': '#ffffff'
    },
    'dark': {
        'bg': '#2b2b2b',
        'fg': '#ffffff',
        'button_bg': '#404040',
        'entry_bg': '#404040'
    }
}

def apply_theme(self, theme_name):
    """Aplikuje motyw"""
    theme = THEMES.get(theme_name, THEMES['light'])
    
    self.root.configure(bg=theme['bg'])
    # Apply to all widgets...
```

## 🔄 Auto-save & Recovery

### Auto-save State
```python
def setup_autosave(self):
    """Konfiguruje automatyczny zapis"""
    def autosave():
        if self.bot.driver:
            self.bot.save_browser_state()
        # Schedule next autosave
        self.root.after(300000, autosave)  # 5 minutes
    
    # Start autosave timer
    self.root.after(300000, autosave)
```

### Crash Recovery
```python
def on_closing(self):
    """Obsługuje zamykanie aplikacji"""
    try:
        # Save current state
        self.bot.save_browser_state()
        
        # Save conversation history
        self.history.save_to_file()
        
        # Close browser
        self.bot.close_browser()
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
    finally:
        self.root.destroy()
```