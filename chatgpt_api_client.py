import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import json
import uuid
from typing import Optional


class ChatGPTAPIClient:
    def __init__(self, api_base_url: str = "http://localhost:8008"):
        """Initialize API client"""
        self.api_base_url = api_base_url.rstrip('/')
        self.session_id = None
        self.session = requests.Session()
        self.polling_active = False
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the Tkinter GUI"""
        self.root = tk.Tk()
        self.root.title("ChatGPT Bot API Client")
        self.root.geometry("900x700")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # API Connection frame
        api_frame = ttk.LabelFrame(main_frame, text="API Connection", padding="5")
        api_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)
        
        ttk.Label(api_frame, text="API Server:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.api_url_entry = tk.Entry(api_frame, width=40)
        self.api_url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.api_url_entry.insert(0, self.api_base_url)
        
        self.connect_btn = ttk.Button(api_frame, text="Connect & Create Session", command=self.connect_to_api)
        self.connect_btn.grid(row=0, column=2)
        
        # Session info
        self.session_label = ttk.Label(api_frame, text="Session: Not connected", foreground="red")
        self.session_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Status display
        ttk.Label(main_frame, text="Status & Logs:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.status_text = scrolledtext.ScrolledText(main_frame, height=10, state='disabled')
        self.status_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        self.launch_btn = ttk.Button(button_frame, text="Launch Browser", command=self.launch_browser, state='disabled')
        self.launch_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.load_state_btn = ttk.Button(button_frame, text="Load Browser State", command=self.load_browser_state, state='disabled')
        self.load_state_btn.grid(row=0, column=1, padx=5)
        
        self.save_state_btn = ttk.Button(button_frame, text="Save Browser State", command=self.save_browser_state, state='disabled')
        self.save_state_btn.grid(row=0, column=2, padx=5)
        
        self.close_btn = ttk.Button(button_frame, text="Close Browser", command=self.close_browser, state='disabled')
        self.close_btn.grid(row=0, column=3, padx=(5, 0))
        
        # Status polling control
        self.auto_refresh_var = tk.BooleanVar(value=True)
        self.auto_refresh_cb = ttk.Checkbutton(button_frame, text="Auto-refresh status", variable=self.auto_refresh_var)
        self.auto_refresh_cb.grid(row=0, column=4, padx=(15, 0))
        
        # Question input
        ttk.Label(main_frame, text="Question:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.question_entry = tk.Entry(main_frame, width=50)
        self.question_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.question_entry.insert(0, "What is Pydantic AI?")
        
        self.ask_btn = ttk.Button(main_frame, text="Ask Question", command=self.ask_question, state='disabled')
        self.ask_btn.grid(row=5, column=1, padx=(10, 0), pady=(0, 5))
        
        # Clear response button
        self.clear_response_btn = ttk.Button(main_frame, text="Clear Response", command=self.clear_response)
        self.clear_response_btn.grid(row=6, column=1, padx=(10, 0), pady=(5, 0), sticky=tk.E)
        
        # Response display
        ttk.Label(main_frame, text="Response:").grid(row=6, column=0, sticky=tk.W, pady=(10, 5))
        self.response_text = scrolledtext.ScrolledText(main_frame, height=15, state='disabled')
        self.response_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(7, weight=2)
        
        # Bind Enter key to question entry
        self.question_entry.bind('<Return>', lambda e: self.ask_question())
        
        # Start status polling
        self.start_status_polling()
        
    def log_status(self, message):
        """Add status message to the status display"""
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.status_text.config(state='disabled')
        self.status_text.see(tk.END)
        self.root.update()
    
    def update_response_display(self, text):
        """Update the response display with new text"""
        self.response_text.config(state='normal')
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(1.0, text)
        self.response_text.config(state='disabled')
        self.response_text.see(tk.END)
        self.root.update()
    
    def clear_response(self):
        """Clear the response display"""
        self.response_text.config(state='normal')
        self.response_text.delete(1.0, tk.END)
        self.response_text.config(state='disabled')
        
    def make_api_request(self, method: str, endpoint: str, data: dict = None) -> Optional[dict]:
        """Make API request with error handling"""
        try:
            url = f"{self.api_base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            self.log_status("❌ Cannot connect to API server. Is the server running?")
            return None
        except requests.exceptions.HTTPError as e:
            self.log_status(f"❌ API Error {response.status_code}: {response.text}")
            return None
        except Exception as e:
            self.log_status(f"❌ Request error: {str(e)}")
            return None
    
    def connect_to_api(self):
        """Connect to API and create new session"""
        def connect_thread():
            self.connect_btn.config(state='disabled')
            
            # Update API base URL
            self.api_base_url = self.api_url_entry.get().strip().rstrip('/')
            
            # Test API connection
            self.log_status("🔗 Connecting to API server...")
            result = self.make_api_request("GET", "/")
            
            if result:
                self.log_status(f"✅ Connected to API: {result.get('message', 'Unknown')}")
                
                # Create new session
                self.log_status("🆕 Creating new bot session...")
                create_result = self.make_api_request("POST", "/bot/create")
                
                if create_result:
                    self.session_id = create_result['session_id']
                    self.log_status(f"✅ Session created: {self.session_id}")
                    self.session_label.config(text=f"Session: {self.session_id}", foreground="green")
                    
                    # Enable control buttons
                    self.launch_btn.config(state='normal')
                    self.load_state_btn.config(state='normal')
                    self.save_state_btn.config(state='normal')
                    self.close_btn.config(state='normal')
                    self.ask_btn.config(state='normal')
                else:
                    self.connect_btn.config(state='normal')
            else:
                self.connect_btn.config(state='normal')
                
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def launch_browser(self):
        """Launch browser via API"""
        if not self.session_id:
            messagebox.showerror("Error", "No active session. Please connect first.")
            return
            
        def launch_thread():
            self.launch_btn.config(state='disabled')
            self.log_status("🚀 Launching browser...")
            
            result = self.make_api_request("POST", "/bot/launch", {"session_id": self.session_id})
            if result:
                self.log_status("✅ Browser launch initiated")
            
            self.launch_btn.config(state='normal')
                
        threading.Thread(target=launch_thread, daemon=True).start()
        
    def load_browser_state(self):
        """Load browser state via API"""
        if not self.session_id:
            messagebox.showerror("Error", "No active session. Please connect first.")
            return
            
        def load_thread():
            self.log_status("📂 Loading browser state...")
            
            result = self.make_api_request("POST", "/bot/load_state", {"session_id": self.session_id})
            if result:
                self.log_status("✅ Browser state loading initiated")
                
        threading.Thread(target=load_thread, daemon=True).start()
        
    def save_browser_state(self):
        """Save browser state via API"""
        if not self.session_id:
            messagebox.showerror("Error", "No active session. Please connect first.")
            return
            
        def save_thread():
            self.log_status("💾 Saving browser state...")
            
            result = self.make_api_request("POST", "/bot/save_state", {"session_id": self.session_id})
            if result:
                self.log_status("✅ Browser state saving initiated")
                
        threading.Thread(target=save_thread, daemon=True).start()
        
    def ask_question(self):
        """Ask question via API"""
        if not self.session_id:
            messagebox.showerror("Error", "No active session. Please connect first.")
            return
            
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question")
            return
            
        def ask_thread():
            self.ask_btn.config(state='disabled')
            self.clear_response()
            self.log_status(f"❓ Asking: {question}")
            
            result = self.make_api_request("POST", "/bot/ask", {
                "session_id": self.session_id,
                "question": question
            })
            
            if result:
                self.log_status("✅ Question submitted, waiting for response...")
                # Response will be shown via status polling
            
            self.ask_btn.config(state='normal')
                
        threading.Thread(target=ask_thread, daemon=True).start()
        
    def close_browser(self):
        """Close browser via API"""
        if not self.session_id:
            messagebox.showerror("Error", "No active session. Please connect first.")
            return
            
        def close_thread():
            self.log_status("🔒 Closing browser...")
            
            result = self.make_api_request("POST", "/bot/close", {"session_id": self.session_id})
            if result:
                self.log_status("✅ Browser close initiated")
                
        threading.Thread(target=close_thread, daemon=True).start()
        
    def start_status_polling(self):
        """Start polling API for status updates"""
        def poll_status():
            last_response = None
            if self.session_id and self.auto_refresh_var.get():
                result = self.make_api_request("GET", f"/bot/status/{self.session_id}")
                if result:
                    # Update logs
                    logs = result.get('logs', [])
                    if logs:
                        # Get last few logs that aren't already displayed
                        current_text = self.status_text.get(1.0, tk.END)
                        for log_entry in logs[-5:]:  # Show last 5 log entries
                            log_line = f"{log_entry['timestamp']} - {log_entry['message']}\n"
                            if log_line not in current_text:
                                self.status_text.config(state='normal')
                                self.status_text.insert(tk.END, log_line)
                                self.status_text.config(state='disabled')
                                self.status_text.see(tk.END)
                    
                    # Update response
                    current_response = result.get('current_response')
                    if current_response and current_response != last_response:
                       last_response = current_response
                       if current_response and current_response.strip():
                           self.update_response_display(current_response)
                           
                           # Save response to file if it's complete
                           if result.get('status') == 'completed':
                               try:
                                   with open("chatgpt_api_answer.txt", "w", encoding="utf-8") as f:
                                       f.write(current_response)
                                   self.log_status("💾 Response saved to chatgpt_api_answer")
                               except Exception as e:
                                   self.log_status(f"❌ Error saving response: {e}")
            
            # Schedule next poll
            if self.polling_active:
                self.root.after(2000, poll_status)  # Poll every 2 seconds
        
        self.polling_active = True
        poll_status()
        
    def stop_status_polling(self):
        """Stop status polling"""
        self.polling_active = False
        
    def cleanup_session(self):
        """Cleanup session on exit"""
        if self.session_id:
            try:
                self.make_api_request("DELETE", f"/bot/{self.session_id}")
                self.log_status(f"🗑️ Session {self.session_id} cleaned up")
            except:
                pass  # Ignore cleanup errors
        
    def on_closing(self):
        """Handle window closing"""
        self.stop_status_polling()
        self.cleanup_session()
        self.root.destroy()
        
    def run(self):
        """Start the GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    print("🚀 Starting ChatGPT Bot API Client...")
    print("💡 Make sure the API server is running on http://localhost:8008")
    
    client = ChatGPTAPIClient()
    client.run()
