import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from chatgpt_bot_core import ChatGPTBot


class ChatGPTGUI:
    def __init__(self):
        self.bot = None
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the Tkinter GUI"""
        self.root = tk.Tk()
        self.root.title("ChatGPT Bot")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Status display
        ttk.Label(main_frame, text="Status:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.status_text = scrolledtext.ScrolledText(main_frame, height=8, state='disabled')
        self.status_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        self.launch_btn = ttk.Button(button_frame, text="Launch Browser", command=self.launch_browser)
        self.launch_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.load_state_btn = ttk.Button(button_frame, text="Load Browser State", command=self.load_browser_state, state='disabled')
        self.load_state_btn.grid(row=0, column=1, padx=5)
        
        self.save_state_btn = ttk.Button(button_frame, text="Save Browser State", command=self.save_browser_state, state='disabled')
        self.save_state_btn.grid(row=0, column=2, padx=5)
        
        self.close_btn = ttk.Button(button_frame, text="Close Browser", command=self.close_browser, state='disabled')
        self.close_btn.grid(row=0, column=3, padx=(5, 0))
        
        # Question input
        ttk.Label(main_frame, text="Question:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.question_entry = tk.Entry(main_frame, width=50)
        self.question_entry.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.question_entry.insert(0, "What is Pydantic AI?")
        
        self.ask_btn = ttk.Button(main_frame, text="Ask Question", command=self.ask_question, state='disabled')
        self.ask_btn.grid(row=4, column=1, padx=(10, 0), pady=(0, 5))
        
        # Clear response button
        self.clear_response_btn = ttk.Button(main_frame, text="Clear Response", command=self.clear_response)
        self.clear_response_btn.grid(row=5, column=1, padx=(10, 0), pady=(5, 0), sticky=tk.E)
        
        # Response display
        ttk.Label(main_frame, text="Response:").grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        self.response_text = scrolledtext.ScrolledText(main_frame, height=15, state='disabled')
        self.response_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=2)
        
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
        
    def launch_browser(self):
        """Launch browser in a separate thread"""
        def launch_thread():
            self.launch_btn.config(state='disabled')
            self.bot = ChatGPTBot(
                status_callback=self.log_status,
                response_callback=self.update_response_display
            )
            
            if self.bot.launch_browser():
                self.load_state_btn.config(state='normal')
                self.save_state_btn.config(state='normal')
                self.close_btn.config(state='normal')
                self.ask_btn.config(state='normal')
                
                # Automatically try to load browser state
                self.bot.load_browser_state()
            else:
                self.launch_btn.config(state='normal')
                
        threading.Thread(target=launch_thread, daemon=True).start()
        
    def load_browser_state(self):
        """Load browser state"""
        def load_thread():
            if self.bot:
                self.bot.load_browser_state()
                
        threading.Thread(target=load_thread, daemon=True).start()
        
    def save_browser_state(self):
        """Save browser state"""
        def save_thread():
            if self.bot:
                self.bot.save_browser_state()
                
        threading.Thread(target=save_thread, daemon=True).start()
        
    def ask_question(self):
        """Ask question in a separate thread"""
        def ask_thread():
            if self.bot:
                question = self.question_entry.get().strip()
                if question:
                    self.ask_btn.config(state='disabled')
                    # Clear response display before starting
                    self.clear_response()
                    
                    response = self.bot.ask_question_and_get_response(question)
                    
                    if response:
                        # Final response update (in case real-time updates missed anything)
                        self.update_response_display(response)
                        
                        # Save response to file
                        try:
                            with open("chatgpt_answer.txt", "w", encoding="utf-8") as f:
                                f.write(response)
                            self.log_status("Response saved to chatgpt_answer.txt")
                        except Exception as e:
                            self.log_status(f"Error saving response: {e}")
                        
                        # Auto-save browser state after successful interaction
                        self.bot.save_browser_state()
                    
                    self.ask_btn.config(state='normal')
                else:
                    messagebox.showwarning("Warning", "Please enter a question")
                    
        threading.Thread(target=ask_thread, daemon=True).start()
        
    def close_browser(self):
        """Close browser"""
        def close_thread():
            if self.bot:
                self.bot.close_browser()
                self.bot = None
                self.launch_btn.config(state='normal')
                self.load_state_btn.config(state='disabled')
                self.save_state_btn.config(state='disabled')
                self.close_btn.config(state='disabled')
                self.ask_btn.config(state='disabled')
                
        threading.Thread(target=close_thread, daemon=True).start()
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()
