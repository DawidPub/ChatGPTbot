#!/usr/bin/env python3
"""
ChatGPT Bot Application

This application provides a GUI interface for automating interactions with ChatGPT.
It uses Selenium for web automation and Tkinter for the user interface.

Usage:
    python main.py

Requirements:
    - pip install selenium webdriver-manager
    - Chrome browser installed
"""

from chatgpt_gui import ChatGPTGUI


def main():
    """Main entry point for the ChatGPT Bot application"""
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
