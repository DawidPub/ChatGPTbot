#!/usr/bin/env python3
"""
ChatGPT Bot Application - Compatibility Entry Point

This file maintains backward compatibility with the original single-file structure
while using the new modular design.

The classes have been separated into:
- chatgpt_bot_core.py: Contains the ChatGPTBot class
- chatgpt_gui.py: Contains the ChatGPTGUI class
- main.py: Main entry point for the application

Requirements:
    - pip install selenium webdriver-manager
    - Chrome browser installed
"""

# Import the separated classes for backward compatibility
from chatgpt_bot_core import ChatGPTBot
from chatgpt_gui import ChatGPTGUI


def main():
    """Main entry point for backward compatibility"""
    try:
        # Create and run the GUI application
        app = ChatGPTGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error starting application: {e}")
        raise


if __name__ == "__main__":
    main()