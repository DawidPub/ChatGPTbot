# pip install selenium webdriver-manager
import os, time, json, pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class ChatGPTBot:
    def __init__(self, status_callback=None, response_callback=None):
        self.driver = None
        self.wait = None
        self.cookies_file = "chatgpt_cookies.pkl"
        self.session_file = "chatgpt_session.json"
        self.status_callback = status_callback
        self.response_callback = response_callback
        
    def log_status(self, message):
        """Log status message via callback if provided"""
        if self.status_callback:
            self.status_callback(message)
        else:
            print(message)
    
    def update_response(self, text):
        """Update response display via callback if provided"""
        if self.response_callback:
            self.response_callback(text)
        else:
            print(f"Response: {text}")

    def log_response_line(self, line, line_number=None):
        """Log individual response line"""
        if line_number is not None:
            self.log_status(f"Line {line_number}: {line[:100]}{'...' if len(line) > 100 else ''}")
        else:
            self.log_status(f"Response line: {line[:100]}{'...' if len(line) > 100 else ''}")

    def launch_browser(self):
        """Launch Chrome browser with optimized settings"""
        try:
            self.log_status("Launching browser...")
            
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 30)
            
            self.log_status("Browser launched successfully")
            return True
            
        except Exception as e:
            self.log_status(f"Error launching browser: {e}")
            return False
            
    def save_browser_state(self):
        """Save cookies and session data"""
        try:
            if not self.driver:
                self.log_status("No browser instance to save state from")
                return False
                
            # Save cookies
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, 'wb') as f:
                pickle.dump(cookies, f)
            self.log_status(f"Cookies saved to {self.cookies_file}")
            
            # Save session data (localStorage and sessionStorage)
            session_data = {
                'localStorage': self.driver.execute_script("return Object.assign({}, localStorage);"),
                'sessionStorage': self.driver.execute_script("return Object.assign({}, sessionStorage);"),
                'current_url': self.driver.current_url
            }
            
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2)
            self.log_status(f"Session data saved to {self.session_file}")
            return True
            
        except Exception as e:
            self.log_status(f"Error saving browser state: {e}")
            return False

    def load_browser_state(self):
        """Load cookies and session data"""
        try:
            if not self.driver:
                self.log_status("No browser instance to load state into")
                return False
                
            # First navigate to the domain to set cookies
            self.log_status("Opening ChatGPT...")
            self.driver.get("https://chatgpt.com")
            # time.sleep(2)
            
            # Load cookies if they exist
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'rb') as f:
                    cookies = pickle.load(f)
                
                for cookie in cookies:
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        self.log_status(f"Could not add cookie {cookie.get('name', 'unknown')}: {e}")
                
                self.log_status(f"Cookies loaded from {self.cookies_file}")
                
                # Refresh page to apply cookies
                self.driver.refresh()
                time.sleep(3)
            
            # Load session data if it exists
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # Restore localStorage
                if 'localStorage' in session_data:
                    for key, value in session_data['localStorage'].items():
                        try:
                            self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
                        except Exception as e:
                            self.log_status(f"Could not set localStorage item {key}: {e}")
                
                # Restore sessionStorage
                if 'sessionStorage' in session_data:
                    for key, value in session_data['sessionStorage'].items():
                        try:
                            self.driver.execute_script(f"sessionStorage.setItem('{key}', '{value}');")
                        except Exception as e:
                            self.log_status(f"Could not set sessionStorage item {key}: {e}")
                
                self.log_status(f"Session data loaded from {self.session_file}")
                
                # Refresh again to apply session data
                self.driver.refresh()
                time.sleep(3)
                
                self.log_status("Page loaded successfully (restored session)")
            else:
                self.log_status("Page loaded successfully (fresh session)")
            
            # Check if already logged in by looking for chat interface
            try:
                # Try to find the prompt textarea (indicates logged in)
                prompt_element = self.driver.find_element(By.ID, "prompt-textarea")
                self.log_status("Already logged in - session restored successfully!")
                return True
            except:
                self.log_status("Not logged in - you may need to log in manually")
                time.sleep(3)
                return True
            
        except Exception as e:
            self.log_status(f"Error loading browser state: {e}")
            return False

    def ask_question_and_get_response(self, query):
        """Ask a question and wait for the complete response"""
        try:
            if not self.driver or not self.wait:
                self.log_status("Browser not initialized")
                return None
                
            # Ask the question
            self.log_status(f"Asking question: {query}")
            prompt = self.wait.until(EC.element_to_be_clickable((By.ID, "prompt-textarea")))
            prompt.send_keys(query, Keys.RETURN)

            # Wait for the response with improved logic
            self.log_status("Waiting for ChatGPT response...")
            
            # Wait for any response to appear and complete
            response_appeared = False
            response_completed = False
            max_attempts = 120  # 2 minutes total wait time
            previous_text = ""
            stable_count = 0
            
            for attempt in range(max_attempts):
                try:
                    # Look for response elements with multiple possible selectors
                    possible_selectors = [
                        "div[data-message-author-role='assistant'] div.markdown",
                        "div[data-message-author-role='assistant']",
                        ".text-message",
                        "[data-testid*='conversation-turn']"
                    ]
                    
                    current_text = ""
                    for selector in possible_selectors:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            last_element = elements[-1]
                            current_text = last_element.text.strip()
                            if current_text:
                                response_appeared = True
                                break
                    
                    # Check if response has appeared
                    if response_appeared:
                        # Update response display in real-time
                        if current_text and current_text != previous_text:
                            self.update_response(current_text)
                            
                            # Log each line of the response
                            lines = current_text.split('\n')
                            for line_num, line in enumerate(lines, 1):
                                if line.strip():  # Only log non-empty lines
                                    self.log_response_line(line.strip(), line_num)
                        
                        # Check if the response is still being generated
                        # Look for typing indicators or "stop generating" button
                        stop_button = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='stop-button'], button[aria-label='Stop generating']")
                        typing_indicator = self.driver.find_elements(By.CSS_SELECTOR, ".result-streaming, [data-testid='typing-indicator']")
                        
                        # If there's a stop button or typing indicator, response is still being generated
                        if stop_button or typing_indicator:
                            self.log_status(f"Attempt {attempt + 1}: Response is being generated...")
                            previous_text = current_text
                            stable_count = 0
                        else:
                            # No typing indicators, check if text has stabilized
                            if current_text == previous_text and current_text:
                                stable_count += 1
                                self.log_status(f"Attempt {attempt + 1}: Text stable for {stable_count} seconds")
                                
                                # Consider response complete if text hasn't changed for 3 consecutive checks
                                if stable_count >= 3:
                                    response_completed = True
                                    self.log_status("Response appears to be complete!")
                                    break
                            else:
                                # Text is still changing
                                self.log_status(f"Attempt {attempt + 1}: Response text is still changing...")
                                if current_text:  # Update display with current text
                                    self.update_response(current_text)
                                previous_text = current_text
                                stable_count = 0
                    else:
                        self.log_status(f"Attempt {attempt + 1}: Waiting for response to appear...")
                        
                    time.sleep(1)
                    
                except Exception as e:
                    self.log_status(f"Attempt {attempt + 1}: {e}")
                    time.sleep(1)
            
            if not response_appeared:
                self.log_status("No response found, trying fallback method...")
                # Fallback: get all text content from the page
                all_content = self.driver.find_element(By.TAG_NAME, "body").text
                answer = "Response timeout - Full page content:\n" + all_content
            elif not response_completed:
                self.log_status("Response appeared but may not be complete, extracting current text...")
                # Get the response text even if we're not sure it's complete
                try:
                    # Try multiple selectors to get the answer text
                    answer = None
                    for selector in possible_selectors:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            answer = elements[-1].text.strip()
                            if answer:
                                break
                    
                    if not answer:
                        answer = "Could not extract response text"
                    else:
                        answer = "[WARNING: Response may be incomplete]\n\n" + answer
                        # Update response display with warning
                        self.update_response(answer)
                        
                        # Log incomplete response line by line
                        self.log_status("Incomplete response - logging available lines:")
                        lines = answer.split('\n')[2:]  # Skip warning lines
                        for line_num, line in enumerate(lines, 1):
                            if line.strip():
                                self.log_response_line(line.strip(), line_num)
                        
                except Exception as e:
                    answer = f"Error extracting response: {e}"
            else:
                # Get the complete response text
                try:
                    # Try multiple selectors to get the answer text
                    answer = None
                    for selector in possible_selectors:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            answer = elements[-1].text.strip()
                            if answer:
                                break
                    
                    if not answer:
                        answer = "Could not extract response text"
                    else:
                        # Final update of response display
                        self.update_response(answer)
                        
                        # Log final response line by line
                        self.log_status("Final response received - logging all lines:")
                        lines = answer.split('\n')
                        for line_num, line in enumerate(lines, 1):
                            if line.strip():  # Only log non-empty lines
                                self.log_response_line(line.strip(), line_num)
                        
                except Exception as e:
                    answer = f"Error extracting response: {e}"
            
            self.log_status("Response received successfully")
            return answer
            
        except Exception as e:
            self.log_status(f"Error asking question: {e}")
            return None
    
    def close_browser(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
                self.log_status("Browser closed successfully")
                return True
            else:
                self.log_status("No browser instance to close")
                return True
        except Exception as e:
            self.log_status(f"Error closing browser: {e}")
            return False
