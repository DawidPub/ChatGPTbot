import subprocess
import time
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os

class APILauncher:
    def __init__(self):
        self.server_process = None
        self.client_process = None
        self.setup_gui()
        
    def setup_gui(self):
        """Setup launcher GUI"""
        self.root = tk.Tk()
        self.root.title("ChatGPT Bot API Launcher")
        self.root.geometry("730x650")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🚀 ChatGPT Bot API Launcher", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Server section
        server_frame = ttk.LabelFrame(main_frame, text="API Server", padding="10")
        server_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        server_frame.columnconfigure(1, weight=1)
        
        self.server_status_label = ttk.Label(server_frame, text="Status: Not running", foreground="red")
        self.server_status_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        self.start_server_btn = ttk.Button(server_frame, text="Start API Server", command=self.start_server)
        self.start_server_btn.grid(row=1, column=0, pady=(10, 0), padx=(0, 10))
        
        self.stop_server_btn = ttk.Button(server_frame, text="Stop API Server", command=self.stop_server, state='disabled')
        self.stop_server_btn.grid(row=1, column=1, pady=(10, 0), sticky=tk.W)
        
        # Client section
        client_frame = ttk.LabelFrame(main_frame, text="API Client", padding="10")
        client_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        client_frame.columnconfigure(1, weight=1)
        
        self.client_status_label = ttk.Label(client_frame, text="Status: Not running", foreground="red")
        self.client_status_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        self.start_client_btn = ttk.Button(client_frame, text="Start API Client", command=self.start_client)
        self.start_client_btn.grid(row=1, column=0, pady=(10, 0), padx=(0, 10))
        
        self.stop_client_btn = ttk.Button(client_frame, text="Stop API Client", command=self.stop_client, state='disabled')
        self.stop_client_btn.grid(row=1, column=1, pady=(10, 0), sticky=tk.W)
        
        # Quick start section
        quick_frame = ttk.LabelFrame(main_frame, text="Quick Start", padding="10")
        quick_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_both_btn = ttk.Button(quick_frame, text="🚀 Start Both (Server + Client)", command=self.start_both, style='Accent.TButton')
        self.start_both_btn.grid(row=0, column=0, pady=5)
        
        self.stop_all_btn = ttk.Button(quick_frame, text="⏹️ Stop All", command=self.stop_all, state='disabled')
        self.stop_all_btn.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Dependencies info
        deps_frame = ttk.LabelFrame(main_frame, text="Dependencies", padding="10")
        deps_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        deps_text = ("Required packages: fastapi, uvicorn, pydantic, requests\n"
                    "Install with: pip install fastapi uvicorn pydantic requests")
        deps_label = ttk.Label(deps_frame, text=deps_text, justify=tk.LEFT)
        deps_label.grid(row=0, column=0, sticky=tk.W)
        
        self.install_deps_btn = ttk.Button(deps_frame, text="Install Dependencies", command=self.install_dependencies)
        self.install_deps_btn.grid(row=1, column=0, pady=(10, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, state='disabled')
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Start status monitoring
        self.monitor_processes()
        
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)
        self.root.update()
        
    def install_dependencies(self):
        """Install required dependencies"""
        def install_thread():
            self.install_deps_btn.config(state='disabled')
            self.log("📦 Installing dependencies...")
            
            try:
                # Install packages
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", 
                    "fastapi", "uvicorn", "pydantic", "requests"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log("✅ Dependencies installed successfully!")
                else:
                    self.log(f"❌ Error installing dependencies: {result.stderr}")
                    
            except Exception as e:
                self.log(f"❌ Error installing dependencies: {e}")
            
            self.install_deps_btn.config(state='normal')
            
        threading.Thread(target=install_thread, daemon=True).start()
        
    def start_server(self):
        """Start API server"""
        if self.server_process and self.server_process.poll() is None:
            self.log("⚠️ Server is already running")
            return
            
        try:
            self.log("🚀 Starting API server...")
            self.server_process = subprocess.Popen([
                sys.executable, "chatgpt_api_server.py"
            ], cwd=os.getcwd())
            
            self.start_server_btn.config(state='disabled')
            self.stop_server_btn.config(state='normal')
            self.log("✅ API server started")
            
            # Wait a moment then check if server is responding
            def check_server():
                time.sleep(3)
                try:
                    response = requests.get("http://localhost:8000/", timeout=5)
                    if response.status_code == 200:
                        self.log("✅ API server is responding")
                    else:
                        self.log("⚠️ API server started but not responding correctly")
                except:
                    self.log("⚠️ API server may not be responding yet")
                    
            threading.Thread(target=check_server, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Error starting server: {e}")
            
    def stop_server(self):
        """Stop API server"""
        if self.server_process:
            try:
                self.log("⏹️ Stopping API server...")
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                self.log("✅ API server stopped")
            except subprocess.TimeoutExpired:
                self.log("🔪 Force killing API server...")
                self.server_process.kill()
                self.log("✅ API server force stopped")
            except Exception as e:
                self.log(f"❌ Error stopping server: {e}")
                
            self.server_process = None
            
        self.start_server_btn.config(state='normal')
        self.stop_server_btn.config(state='disabled')
        
    def start_client(self):
        """Start API client"""
        if self.client_process and self.client_process.poll() is None:
            self.log("⚠️ Client is already running")
            return
            
        try:
            self.log("🚀 Starting API client...")
            self.client_process = subprocess.Popen([
                sys.executable, "chatgpt_api_client.py"
            ], cwd=os.getcwd())
            
            self.start_client_btn.config(state='disabled')
            self.stop_client_btn.config(state='normal')
            self.log("✅ API client started")
            
        except Exception as e:
            self.log(f"❌ Error starting client: {e}")
            
    def stop_client(self):
        """Stop API client"""
        if self.client_process:
            try:
                self.log("⏹️ Stopping API client...")
                self.client_process.terminate()
                self.client_process.wait(timeout=5)
                self.log("✅ API client stopped")
            except subprocess.TimeoutExpired:
                self.log("🔪 Force killing API client...")
                self.client_process.kill()
                self.log("✅ API client force stopped")
            except Exception as e:
                self.log(f"❌ Error stopping client: {e}")
                
            self.client_process = None
            
        self.start_client_btn.config(state='normal')
        self.stop_client_btn.config(state='disabled')
        
    def start_both(self):
        """Start both server and client"""
        def start_sequence():
            # Start server first
            self.start_server()
            
            # Wait for server to be ready
            self.log("⏳ Waiting for server to be ready...")
            for i in range(10):
                try:
                    response = requests.get("http://localhost:8000/", timeout=2)
                    if response.status_code == 200:
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.log("⚠️ Server may not be ready, starting client anyway...")
            
            # Start client
            time.sleep(1)
            self.start_client()
            
            self.start_both_btn.config(state='disabled')
            self.stop_all_btn.config(state='normal')
            
        threading.Thread(target=start_sequence, daemon=True).start()
        
    def stop_all(self):
        """Stop both server and client"""
        self.stop_client()
        self.stop_server()
        
        self.start_both_btn.config(state='normal')
        self.stop_all_btn.config(state='disabled')
        
    def monitor_processes(self):
        """Monitor process status and update UI"""
        # Check server status
        if self.server_process and self.server_process.poll() is None:
            self.server_status_label.config(text="Status: Running", foreground="green")
        else:
            self.server_status_label.config(text="Status: Not running", foreground="red")
            if self.server_process:  # Process ended
                self.start_server_btn.config(state='normal')
                self.stop_server_btn.config(state='disabled')
                
        # Check client status
        if self.client_process and self.client_process.poll() is None:
            self.client_status_label.config(text="Status: Running", foreground="green")
        else:
            self.client_status_label.config(text="Status: Not running", foreground="red")
            if self.client_process:  # Process ended
                self.start_client_btn.config(state='normal')
                self.stop_client_btn.config(state='disabled')
                
        # Update stop all button
        both_running = (self.server_process and self.server_process.poll() is None) or \
                      (self.client_process and self.client_process.poll() is None)
        
        if both_running:
            self.stop_all_btn.config(state='normal')
        else:
            self.stop_all_btn.config(state='disabled')
            self.start_both_btn.config(state='normal')
                
        # Schedule next check
        self.root.after(2000, self.monitor_processes)
        
    def on_closing(self):
        """Handle window closing"""
        self.stop_all()
        time.sleep(1)  # Give processes time to stop
        self.root.destroy()
        
    def run(self):
        """Start launcher"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    print("🚀 ChatGPT Bot API Launcher")
    launcher = APILauncher()
    launcher.run()
