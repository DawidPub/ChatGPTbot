"""
ChatGPT Bot Package

A modular Python application for automating interactions with ChatGPT through a GUI interface.

Classes:
    ChatGPTBot: Core web automation functionality
    ChatGPTGUI: Tkinter-based graphical user interface

Usage:
    # Run the complete application
    from chatgpt_gui import ChatGPTGUI
    app = ChatGPTGUI()
    app.run()
    
    # Use just the automation core
    from chatgpt_bot_core import ChatGPTBot
    bot = ChatGPTBot()
    bot.launch_browser()
    response = bot.ask_question_and_get_response("Hello!")
    bot.close_browser()

Requirements:
    - selenium>=4.0.0
    - webdriver-manager>=3.8.0
    - Chrome browser installed
"""

__version__ = "2.0.0"
__author__ = "ChatGPT Bot Project"
__email__ = ""
__description__ = "Automated ChatGPT interaction with GUI interface"

# Import main classes for convenient access
from .chatgpt_bot_core import ChatGPTBot
from .chatgpt_gui import ChatGPTGUI

# Define what gets imported with "from chatgpt_bot import *"
__all__ = [
    'ChatGPTBot',
    'ChatGPTGUI',
    '__version__'
]
